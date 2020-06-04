import nuke
import nukescripts

filetypeList = ['cin', 'dpx','exr','fpi','hdr','jpg','jpeg','mov','null','pic','png','sgi','tga','tiff','tif','xpm','yuv']


class WatermarkController(object):
    def __init__(self, panel):
        self.panel = panel
        self.file_settings = []
        self.source_read = []
        self.merge_nodes = []
        self.output_write = []
        self.transform_nodes = []

    def add_source(self):
        source = self.panel.sourceKnob.value()
        source = '{} {}'.format(source, nuke.getFileNameList(os.path.dirname(source))[0].split(' ')[1])
        output_format = self.panel.formatKnob.value()
        dest = self.panel.outputKnob.value()
        if not all([source, output_format, dest]):
            return
        data = (source, output_format, dest)
        if data not in self.file_settings:
            self.file_settings.append(data)
        self.panel.sourceKnob.setValue('')
        self.panel.outputKnob.setValue('')

    def transformText(self,read,merge,text,num):
        x1 = read.metadata('input/width')*(17.0/64.0)
        s1 = read.metadata('input/width')*(13.0/32.0)/600
        x2 = read.metadata('input/width')*(1.0/3.0)
        s2 = read.metadata('input/width')*((1.0/3.0)-(1.0/32.0))/600
        y1 = read.metadata('input/height')*(1.0/4.0)
        y2 = read.metadata('input/height')*(1.0/3.0)
        text.knob('box').setValue([0,0,read.metadata('input/width'),read.metadata('input/height')])
        text.knob('xjustify').setValue('center')
        text.knob('yjustify').setValue('center')
        del self.transform_nodes[:]

        if num == 1:
            transform = nuke.nodes.Transform()
            transform.setInput(0,text)
            transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
            transform.knob('scale').setValue(0.5)
            transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
            transform.knob('ori_scale').setValue(0.5)
            merge.setInput(1,transform)

        if num == 2:
            for i in range(2):
                transform = nuke.nodes.Transform()
                transform.setInput(0,text)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s1)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s1)
                self.transform_nodes.append(transform)
                merge.setInput(i+3,transform)
            self.transform_nodes[0].knob('translate').setValue([x1,0])
            self.transform_nodes[1].knob('translate').setValue([-x1,0])

        if num == 3:
            for i in range(3):
                transform = nuke.nodes.Transform()
                transform.setInput(0,text)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s2)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s2)
                self.transform_nodes.append(transform)
                merge.setInput(i+3,transform)
            self.transform_nodes[0].knob('translate').setValue([x2,0])
            self.transform_nodes[1].knob('translate').setValue([-x2,0])

        if num == 4:
            for i in range(4):
                transform = nuke.nodes.Transform()
                transform.setInput(0,text)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s1)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s1)
                self.transform_nodes.append(transform)
                merge.setInput(i+3,transform)
            self.transform_nodes[0].knob('translate').setValue([x1,y1])
            self.transform_nodes[1].knob('translate').setValue([-x1,y1])
            self.transform_nodes[2].knob('translate').setValue([x1,-y1])
            self.transform_nodes[3].knob('translate').setValue([-x1,-y1])

        if num == 6:
            for i in range(6):
                transform = nuke.nodes.Transform()
                transform.setInput(0,text)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s2)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s2)
                self.transform_nodes.append(transform)
                merge.setInput(i+3,transform)
            self.transform_nodes[0].knob('translate').setValue([x2,y1])
            self.transform_nodes[1].knob('translate').setValue([-x2,y1])
            self.transform_nodes[2].knob('translate').setValue([x2,-y1])
            self.transform_nodes[3].knob('translate').setValue([-x2,-y1])
            self.transform_nodes[4].knob('translate').setValue([0,-y1])
            self.transform_nodes[5].knob('translate').setValue([0,y1])

        if num == 9:
            for i in range(9):
                transform = nuke.nodes.Transform()
                transform.setInput(0,text)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s2)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s2)
                self.transform_nodes.append(transform)
                merge.setInput(i+3,transform)
            self.transform_nodes[0].knob('translate').setValue([x2,y1])
            self.transform_nodes[1].knob('translate').setValue([-x2,y1])
            self.transform_nodes[2].knob('translate').setValue([x2,-y1])
            self.transform_nodes[3].knob('translate').setValue([-x2,-y1])
            self.transform_nodes[4].knob('translate').setValue([0,-y1])
            self.transform_nodes[5].knob('translate').setValue([0,y1])
            self.transform_nodes[6].knob('translate').setValue([x2,0])
            self.transform_nodes[7].knob('translate').setValue([-x2,0])


    def transformImage(self,read,merge,image,position,num):
        x1 = read.metadata('input/width')*(17.0/64.0)
        s1 = read.metadata('input/width')*(13.0/32.0)/image.metadata('input/width')
        x2 = read.metadata('input/width')*(1.0/3.0)
        s2 = read.metadata('input/width')*((1.0/3.0)-(1.0/32.0))/image.metadata('input/width')
        y1 = read.metadata('input/height')*(1.0/4.0)
        y2 = read.metadata('input/height')*(1.0/3.0)
        position.knob('translate').setValue([read.metadata('input/width')/2-image.metadata('input/width')/2,read.metadata('input/height')/2-image.metadata('input/height')/2])
        del self.transform_nodes[:]

        if num == 1:
            transform = nuke.nodes.Transform()
            transform.setInput(0,position)
            transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
            transform.knob('scale').setValue(0.5)
            merge.setInput(1,transform)

        if num == 2:
            for i in range(2):
                transform = nuke.nodes.Transform()
                transform.setInput(0,position)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s1)
                self.transform_nodes.append(transform)
                merge.setInput(i+3,transform)
            self.transform_nodes[0].knob('translate').setValue([x1,0])
            self.transform_nodes[1].knob('translate').setValue([-x1,0])

        if num == 3:
            for i in range(3):
                transform = nuke.nodes.Transform()
                transform.setInput(0,position)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s2)
                self.transform_nodes.append(transform)
                merge.setInput(i+3,transform)
            self.transform_nodes[0].knob('translate').setValue([x2,0])
            self.transform_nodes[1].knob('translate').setValue([-x2,0])

        if num == 4:
            for i in range(4):
                transform = nuke.nodes.Transform()
                transform.setInput(0,position)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s1)
                self.transform_nodes.append(transform)
                merge.setInput(i+3,transform)
            self.transform_nodes[0].knob('translate').setValue([x1,y1])
            self.transform_nodes[1].knob('translate').setValue([-x1,y1])
            self.transform_nodes[2].knob('translate').setValue([x1,-y1])
            self.transform_nodes[3].knob('translate').setValue([-x1,-y1])

        if num == 6:
            for i in range(6):
                transform = nuke.nodes.Transform()
                transform.setInput(0,position)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s2)
                self.transform_nodes.append(transform)
                merge.setInput(i+3,transform)
            self.transform_nodes[0].knob('translate').setValue([x2,y1])
            self.transform_nodes[1].knob('translate').setValue([-x2,y1])
            self.transform_nodes[2].knob('translate').setValue([x2,-y1])
            self.transform_nodes[3].knob('translate').setValue([-x2,-y1])
            self.transform_nodes[4].knob('translate').setValue([0,-y1])
            self.transform_nodes[5].knob('translate').setValue([0,y1])

        if num == 9:
            for i in range(9):
                transform = nuke.nodes.Transform()
                transform.setInput(0,position)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s2)
                self.transform_nodes.append(transform)
                merge.setInput(i+3,transform)
            self.transform_nodes[0].knob('translate').setValue([x2,y1])
            self.transform_nodes[1].knob('translate').setValue([-x2,y1])
            self.transform_nodes[2].knob('translate').setValue([x2,-y1])
            self.transform_nodes[3].knob('translate').setValue([-x2,-y1])
            self.transform_nodes[4].knob('translate').setValue([0,-y1])
            self.transform_nodes[5].knob('translate').setValue([0,y1])
            self.transform_nodes[6].knob('translate').setValue([x2,0])
            self.transform_nodes[7].knob('translate').setValue([-x2,0])

    def create_nodes(self):
        index = 0
        for data in self.file_settings:
            readNode = nuke.nodes.Read()
            readNode['file'].fromUserText(data[0])
            self.source_read.append(readNode)
            watermarkMergeNode = nuke.nodes.Merge2()
            watermarkMergeNode.setInput(0,readNode)
            self.merge_nodes.append(watermarkMergeNode)
            writeReformatNode = nuke.nodes.Reformat()
            writeReformatNode.setInput(0,watermarkMergeNode)
            writeReformatNode.knob('format').setValue(data[1])
            writeReformatNode.knob('black_outside').setValue(True)
            watermarkWriteNode = nuke.nodes.Write()
            watermarkWriteNode.setInput(0,writeReformatNode)
            watermarkWriteNode.knob('file').fromUserText(data[2])
            self.output_write.append(watermarkWriteNode)
            nuke.toNode('Viewer1').setInput(index, watermarkWriteNode)
            index += 1

    def watermark_transform(self):
        self.create_nodes()
        for i in range(len(self.file_settings)):
            read = self.source_read[i]
            merge = self.merge_nodes[i]
            num = int(self.panel.watermarkNum.value())
            if self.panel.watermarkType.value() == 'Text' and self.panel.watermarkText.value():
                text = nuke.nodes.Text2()
                text.knob('message').setValue(self.panel.watermarkText.value())
                self.transformText(read,merge,text,num)
            if self.panel.watermarkType.value() == 'Image' and self.panel.watermarkImage.value():
                image = nuke.nodes.Read()
                image['file'].fromUserText(self.panel.watermarkImage.value())
                imagePremultNode = nuke.nodes.Premult()
                imagePremultNode.setInput(0,image)
                position = nuke.nodes.Position()
                position.setInput(0,imagePremultNode)
                self.transformImage(read,merge,image,position,num)


class WatermarkControlPanel(nukescripts.panels.PythonPanel):
    def __init__(self):
        super(WatermarkControlPanel, self).__init__('Watermark Control')
        self.setMinimumSize(600,260)
        self.sourceKnob = nuke.File_Knob('file','Open:')
        self.formatKnob = nuke.Format_Knob('format','Format:')
        self.outputKnob = nuke.File_Knob('file','Save:')
        self.addKnob(self.sourceKnob)
        self.addKnob(self.formatKnob)
        self.addKnob(self.outputKnob)
        self.formatKnob.setValue('HD_720')
        self.addSourceKnob = nuke.PyScript_Knob('add', 'Add')
        self.addKnob(self.addSourceKnob)
        self.watermarkType = nuke.Enumeration_Knob('type','Type:',['Text','Image'])
        self.watermarkText = nuke.String_Knob('text','Text:')
        self.watermarkImage = nuke.File_Knob('image','Image:')
        self.watermarkNum = nuke.Enumeration_Knob('num','Number:',['1   ','2   ','3   ','4   ','6   ','9   '])
        self.watermarkCreate = nuke.PyScript_Knob('create','Create')
        self.watermarkRotate = nuke.Double_Knob('rotate','Rotate:')
        self.watermarkScale = nuke.Double_Knob('scale','Scale:')
        self.watermarkOpacity = nuke.Double_Knob('opacity','Opacity:')
        self.watermarkRotate.setRange(-180,180)
        self.watermarkOpacity.setDefaultValue([1,1])
        self.watermarkScale.setRange(0.3,1.5)
        self.watermarkScale.setDefaultValue([1,1])
        self.addKnob(self.watermarkType)
        self.addKnob(self.watermarkText)
        self.addKnob(self.watermarkImage)
        self.addKnob(self.watermarkNum)
        self.addKnob(self.watermarkCreate)
        self.addKnob(self.watermarkRotate)
        self.addKnob(self.watermarkScale)
        self.addKnob(self.watermarkOpacity)
        self.controller = WatermarkController(self)

    def knobChanged(self, knob):
        if knob == self.addSourceKnob:
            self.controller.add_source()
        if knob == self.watermarkType:
            if self.watermarkType.value() == 'Text':
                self.watermarkText.setEnabled(True)
                self.watermarkImage.setEnabled(False)
            else:
                self.watermarkImage.setEnabled(True)
                self.watermarkText.setEnabled(False)
        if knob == self.watermarkCreate:
            self.controller.watermark_transform()
        for i in nuke.allNodes():
            if i.Class() == 'Transform':
                i.knob('rotate').setValue(self.watermarkRotate.value())
                i.knob('scale').setValue(i.knob('ori_scale').value()*self.watermarkScale.value())
            if i.Class() == 'Merge2':
                i.knob('mix').setValue(self.watermarkOpacity.value())


w = WatermarkControlPanel()
def WatermarkTools():
    w.showModalDialog()

    for i in range(flag):
        nuke.execute(writeNodes[i].knob('name').value(),srcReadNodes[i].knob('first').value(),srcReadNodes[i].knob('last').value(),1)
