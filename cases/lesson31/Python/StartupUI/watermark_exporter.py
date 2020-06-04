import hiero.core
import hiero.core.log as log
import hiero.core.nuke as nuke
import hiero.core.FnNukeHelpersV2 as FnNukeHelpersV2
from hiero.exporters import FnExternalRender
from hiero.exporters.FnTranscodeExporter import TranscodeExporter, TranscodePreset
from hiero.exporters.FnExportUtil import TrackItemExportScriptWriter, trackItemTimeCodeNodeStartFrame, createViewerNode
from hiero.exporters import FnEffectHelpers

def get_watermark_read(image_path, premult=True):
    read = nuke.ReadNode(image_path)
    read.setKnob('premultiplied', premult)
    read.setKnob('first', 1)
    read.setKnob('last', 1)
    read.setKnob('origfirst', 1)
    read.setKnob('origlast', 1)
    read.setKnob('before', 'hold')
    read.setKnob('after', 'hold')
    return read


class WatermarkTranscode(TranscodeExporter):

    def __init__(self, initDict):
        super(WatermarkTranscode, self).__init__(initDict)

    def writeSequenceToScript(self, script):
        # Get the range to set on the Root node. This is the range the nuke script will render by default.
        start, end = self.outputRange()
        log.debug( "TranscodeExporter: rootNode range is %s %s", start, end )

        framerate = self._sequence.framerate()
        dropFrames = self._sequence.dropFrame()
        fps = framerate.toFloat()
        rootNode = self.makeRootNode(start, end, fps)
        script.addNode(rootNode)

        # Add Unconnected additional nodes
        if self._preset.properties()["additionalNodesEnabled"]:
            script.addNode(FnExternalRender.createAdditionalNodes(FnExternalRender.kUnconnected, 
                                                                self._preset.properties()["additionalNodesData"], 
                                                                self._item))

        # Force track items to be reformatted to fit the sequence in this case
        reformatMethod = { 
            "to_type" : nuke.ReformatNode.kCompReformatToSequence,
            "filter": self._preset.properties()["reformat"].get("filter")
        }

        if self._preset.properties()["add_image"]:
            watermark_image = get_watermark_read(self._preset.properties()["watermark_path"], 
                                                 self._preset.properties()["watermark_premult"])
            premult_node = nuke.Node('Premult')
            watermark_transform = nuke.Node('Transform')
            watermark_transform.setKnob('translate', self._preset.properties()["watermark_transform"])
            script.addNode(watermark_image)
            script.addNode(premult_node)
            script.addNode(watermark_transform)

        # Build out the sequence.
        scriptParams = FnNukeHelpersV2.ScriptWriteParameters(includeAnnotations=False,
                                                             includeEffects=self.includeEffects(),
                                                             retimeMethod=self._preset.properties()["method"],
                                                             reformatMethod=reformatMethod,
                                                             additionalNodesCallback=self._buildAdditionalNodes,
                                                             views=self.views())

        script.pushLayoutContext("sequence", self._sequence.name(), disconnected=False)
        sequenceWriter = FnNukeHelpersV2.SequenceScriptWriter(self._sequence, scriptParams)
        sequenceWriter.writeToScript(script,
                                     offset=0,
                                     skipOffline=self._skipOffline,
                                     mediaToSkip=self._mediaToSkip,
                                     disconnected=False,
                                     masterTracks=None)
        script.popLayoutContext()
        script.pushLayoutContext("write", "%s_Render" % self._item.name())

        # Create metadata node
        metadataNode = nuke.MetadataNode(metadatavalues=[("hiero/project", self._projectName), ("hiero/project_guid", self._project.guid())] )

        # Add sequence Tags to metadata
        metadataNode.addMetadataFromTags( self._sequence.tags() )

        # Apply timeline offset to nuke output
        script.addNode(nuke.AddTimeCodeNode(timecodeStart=self._sequence.timecodeStart(), fps=framerate, dropFrames=dropFrames, frame= 0 if self._startFrame is None else self._startFrame))

        # The AddTimeCode field will insert an integer framerate into the metadata, if the framerate is floating point, we need to correct this
        metadataNode.addMetadata([("input/frame_rate", framerate.toFloat())])

        # And next the Write.
        script.addNode(metadataNode)

        # Add Burnin group (if enabled)
        self.addBurninNodes(script)

        if self._preset.properties()["add_image"]:
            merge_node = nuke.MergeNode()
            script.addNode(merge_node)

        # Get the output format, either from the sequence or the preset,  and set it as the root format.
        # If a reformat is specified in the preset, add it immediately before the Write node.
        outputReformatNode = self._sequence.format().addToNukeScript(resize=nuke.ReformatNode.kResizeNone, 
                                                                     black_outside=False)
        self._addReformatNode(script, rootNode, outputReformatNode)

        self.addWriteNodeToScript(script, rootNode, framerate)
        script.addNode(createViewerNode(self._projectSettings))
        script.popLayoutContext()

    def writeClipOrTrackItemToScript(self, script):
        isMovieContainerFormat = self._preset.properties()["file_type"] in ("mov", "mov32", "mov64", "ffmpeg")

        start, end = self.outputRange(ignoreRetimes=True, clampToSource=False)
        unclampedStart = start
        log.debug( "rootNode range is %s %s", start, end )

        firstFrame, lastFrame = start, end
        if self._startFrame is not None:
            firstFrame = self._startFrame

        # if startFrame is negative we can only assume this is intentional
        if start < 0 and (self._startFrame is None or self._startFrame >= 0) and not isMovieContainerFormat:
            # We dont want to export an image sequence with a negative frame numbers
            self.setWarning("%i Frames of handles will result in a negative frame index.\nFirst frame clamped to 0." % self._cutHandles)
            start = 0

        # The clip framerate may be invalid, if so, use parent sequence framerate
        fps, framerate, dropFrames = None, None, False
        if self._sequence:
            framerate = self._sequence.framerate()
            dropFrames = self._sequence.dropFrame()
        if self._clip.framerate().isValid():
            framerate = self._clip.framerate()
            dropFrames = self._clip.dropFrame()
        if framerate:
            fps = framerate.toFloat()

        # Create root node, this defines global frame range and framerate
        rootNode = self.makeRootNode(start, end, fps)
        script.addNode(rootNode)

        if self._preset.properties()["add_image"]:
            watermark_image = get_watermark_read(self._preset.properties()["watermark_path"], self._preset.properties()["watermark_premult"])
            premult_node = nuke.Node('Premult')
            watermark_transform = nuke.Node('Transform')
            watermark_transform.setKnob('translate', self._preset.properties()["watermark_transform"])
            script.addNode(watermark_image)
            script.addNode(premult_node)
            script.addNode(watermark_transform)

        # Add Unconnected additional nodes
        if self._preset.properties()["additionalNodesEnabled"]:
            script.addNode(FnExternalRender.createAdditionalNodes(FnExternalRender.kUnconnected, self._preset.properties()["additionalNodesData"], self._item))

        # Now add the Read node.
        writingClip = isinstance(self._item, hiero.core.Clip)
        if writingClip:
            script.pushLayoutContext("clip", self._item.name())
            self._clip.addToNukeScript(script,
                                       additionalNodesCallback=self._buildAdditionalNodes,
                                       firstFrame=firstFrame,
                                       trimmed=True,
                                       includeEffects= self.includeEffects(),
                                       project = self._project) # _clip has no project set, but one is needed by addToNukeScript to do colorpsace conversions
            script.popLayoutContext()
        else:
            # If there are separate track items for each view, write them out (in reverse
            # order so the inputs are correct) then add a JoinViews
            items = self._multiViewTrackItems if self._multiViewTrackItems else [self._item]
            for item in reversed(items):
                script.pushLayoutContext("clip", item.name())
                # Construct a TrackItemExportScriptWriter and write the track item
                trackItemWriter = TrackItemExportScriptWriter(item)
                trackItemWriter.setAdditionalNodesCallback(self._buildAdditionalNodes)
                # Find sequence level effects/annotations which apply to the track item.
                # Annotations are not currently included by the transcode exporter
                effects, annotations = FnEffectHelpers.findEffectsAnnotationsForTrackItems( [item] )
                trackItemWriter.setEffects(self.includeEffects(), effects)

                # TODO This is being done in both the NukeShotExporter and TranscodeExporter.
                # There should be fully shared code for doing the handles calculations.
                fullClipLength = (self._cutHandles is None)
                if fullClipLength:
                    trackItemWriter.setOutputClipLength()
                else:
                    trackItemWriter.setOutputHandles(*self.outputHandles())

                trackItemWriter.setIncludeRetimes(self._retime, self._preset.properties()["method"])
                trackItemWriter.setReformat(self._preset.properties()["reformat"])
                trackItemWriter.setFirstFrame(firstFrame)
                trackItemWriter.writeToScript(script)
                

                if self._preset.properties()["add_image"]:
                    merge_node = nuke.MergeNode()
                    script.addNode(merge_node)

                script.popLayoutContext()

            if self._multiViewTrackItems:
                joinViewsNode = nuke.Node("JoinViews", inputs=len(self.views()))
                script.addNode(joinViewsNode)

        script.pushLayoutContext("write", "%s_Render" % self._item.name())

        metadataNode = nuke.MetadataNode(metadatavalues=[("hiero/project", self._projectName), ("hiero/project_guid", self._project.guid())] )

        # Add sequence Tags to metadata
        metadataNode.addMetadataFromTags( self._clip.tags() )

        # Need a framerate inorder to create a timecode
        if framerate:
            # Apply timeline offset to nuke output
            if self._cutHandles is None:
                timeCodeNodeStartFrame = unclampedStart
            else:
                startHandle, endHandle = self.outputHandles()
                timeCodeNodeStartFrame = trackItemTimeCodeNodeStartFrame(unclampedStart, self._item, startHandle, endHandle)

            script.addNode(nuke.AddTimeCodeNode(timecodeStart=self._clip.timecodeStart(), fps=framerate, dropFrames=dropFrames, frame=timeCodeNodeStartFrame))

            # The AddTimeCode field will insert an integer framerate into the metadata, if the framerate is floating point, we need to correct this
            metadataNode.addMetadata([("input/frame_rate",framerate.toFloat())])

        script.addNode(metadataNode)

        # Add Burnin group (if enabled)
        self.addBurninNodes(script)

        # Get the output format, either from the clip or the preset,  and set it as the root format.
        # If a reformat is specified in the preset, add it immediately before the Write node.
        reformatNode = self._clip.format().addToNukeScript(None)
        self._addReformatNode(script,rootNode,reformatNode)
        self.addWriteNodeToScript(script, rootNode, framerate)
        script.addNode(createViewerNode(self._projectSettings))
        script.popLayoutContext()


class WatermarkTranscodePreset(TranscodePreset):
    def __init__(self, name, properties):
        super(WatermarkTranscodePreset, self).__init__(name, properties)
        self._parentType = WatermarkTranscode


# Register this CustomTask and its associated Preset
hiero.core.taskRegistry.registerTask(WatermarkTranscodePreset, WatermarkTranscode)
