import hiero

from build_track import utils


def get_selected_video_trackitems():
    view = hiero.ui.activeView()
    if not hasattr(view, 'selection'):
        return []
    selection = view.selection()
    if not selection:
        return []

    shot_selection = [item for item in selection
                      if isinstance(item, hiero.core.TrackItem) and
                      isinstance(item.parent(), hiero.core.VideoTrack)]
    track_selection = [item for item in selection
                       if isinstance(item, hiero.core.VideoTrack)]

    if shot_selection and track_selection:
        return []

    if track_selection:
        for track in track_selection:
            shot_selection.extend(track.items())

    return shot_selection


def create_trackitem(track, item_name, clip=None, align_item=None):
    new_trackitem = track.createTrackItem(item_name)

    if clip:
        new_trackitem.setSource(clip)
        new_trackitem.setSourceIn(new_trackitem.sourceIn())

    if align_item:
        if clip:
            duration = align_item.duration()
            new_trackitem.setPlaybackSpeed(align_item.playbackSpeed())
            new_trackitem.setSourceOut(new_trackitem.sourceIn() + duration - 1)
        new_trackitem.setTimelineIn(align_item.timelineIn())
        new_trackitem.setTimelineOut(align_item.timelineOut())

    track.addItem(new_trackitem)
    return new_trackitem


def add_new_videotrack(active_sequence, track_name, added_tracks):
    new_track = hiero.core.VideoTrack(track_name)
    if track_name not in added_tracks:
        added_tracks[track_name] = new_track
        active_sequence.addTrack(new_track)


def get_imported_bin(project, trackitem):
    imported_bin = next((x for x in project.clipsBin().bins()
                         if x.name() == '{}_imported_clips'
                         .format(trackitem.name().split('_')[0])), None)
    if not imported_bin:
        imported_bin = hiero.core.Bin('{}_imported_clips'
                                      .format(trackitem.name().split('_')[0]))
        project.clipsBin().addItem(imported_bin)
    return imported_bin


def create_version_binitems(versions, version_bin):
    new_binitems = []
    for version in versions:
        new_mediasource = hiero.core.MediaSource(version)
        new_clip = hiero.core.Clip(new_mediasource)
        new_clip.setFramerate(hiero.ui.activeSequence().framerate()
                              if hiero.ui.activeSequence()
                              else hiero.core.TimeBase(24.0))
        new_clip.setName(new_clip.name().lower())
        new_binitem = hiero.core.BinItem(new_clip)
        if new_binitem.name() not in [x.name() for x in version_bin.items()]:
            version_bin.addItem(new_binitem)
            new_binitems.append(new_binitem)
        else:
            new_binitems.append([x for x in version_bin.items()
                                 if x.name() == new_binitem.name()][0])

    return new_binitems


def prepare_build_items(project, versions_dict):
    result = []
    if versions_dict:
        for trackitem in versions_dict:
            versions = versions_dict[trackitem][1]
            imported_bin = get_imported_bin(project, trackitem)
            new_binitems = create_version_binitems(versions,
                                                   imported_bin)
            result.append((versions_dict[trackitem][0], new_binitems))
    return result


class BuildTrackProcess(object):
    def __init__(self, project_name):
        super(BuildTrackProcess, self).__init__()
        self._added_tracks = {}
        self.project_name = project_name
        self._active_sequence = hiero.ui.activeSequence()
        self.trackitem_count = 0

    def _build_new_track(self, track_name):
        add_new_videotrack(self._active_sequence,
                           track_name,
                           self._added_tracks)

    def _build_new_trackitem(self, bin_item, parent_trackitems, track_name):
        clip = bin_item.activeItem()
        for item in parent_trackitems:
            create_trackitem(self._added_tracks[track_name],
                             bin_item.name(),
                             clip,
                             item)
            self.trackitem_count += 1

    def _shot_build_process(self, parent_trackitems, bin_items):
        for bin_item in bin_items:
            track_name = utils.get_track_name(bin_item.name())
            self._build_new_track(track_name)
            self._build_new_trackitem(bin_item, parent_trackitems, track_name)

    def buildtrack_process(self, project, import_list):
        with project.beginUndo('Build New Track'):
            for parent_trackitems, bin_items in import_list:
                self._shot_build_process(parent_trackitems, bin_items)
            return self.trackitem_count
