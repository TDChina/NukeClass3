import nuke
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from nukescripts import panels

#initialize lists for storing nodes
srcReadNodes = [] 
mergeNodes = []   
writeNodes = []   
transformNodes = [] 

#flag is the number of source clips
flag = 0

#two lists for storing frame range of rendering
renderFirst = []
renderLast = []

filetypeList = ['cin', 'dpx','exr','fpi','hdr','jpg','jpeg','mov','mp4','null','pic','png','sgi','tga','tiff','tif','xpm','yuv'] #legal output file extention

class WatermarkControlPanel(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setLayout(QtGui.QVBoxLayout()) #vertical layout
        self.setMaximumHeight(360) #tools panel size
        self.setMinimumWidth(400)

        #create all widgets and layouts
        sourceLayout = QtGui.QHBoxLayout() #horizontal layout
        self.sourceLabel = QtGui.QLabel()
        self.sourcePath = QtGui.QLineEdit()
        self.sourceButton = QtGui.QPushButton()
        renderRangeLayout = QtGui.QHBoxLayout()
        formatLayout = QtGui.QHBoxLayout()
        self.formatLabel = QtGui.QLabel()        
        self.formatCombo = QtGui.QComboBox()
        self.nameLabel = QtGui.QLabel()
        self.formatName = QtGui.QLineEdit()
        self.wLabel = QtGui.QLabel()
        self.formatw = QtGui.QLineEdit()
        self.hLabel = QtGui.QLabel()
        self.formath = QtGui.QLineEdit()
        self.outputLabel = QtGui.QLabel()
        self.outputPath = QtGui.QLineEdit()
        self.outputButton = QtGui.QPushButton()
        outputLayout = QtGui.QHBoxLayout()
        self.addclip = QtGui.QPushButton()
        self.typeLabel = QtGui.QLabel()
        self.typeCombo = QtGui.QComboBox()
        self.textLabel = QtGui.QLabel()
        self.watermarkText = QtGui.QLineEdit()
        self.imageLabel = QtGui.QLabel()
        self.watermarkImage = QtGui.QLineEdit()
        self.imageButton = QtGui.QPushButton()
        typeLayout = QtGui.QHBoxLayout()
        textLayout = QtGui.QHBoxLayout()
        imageLayout = QtGui.QHBoxLayout()
        self.numberLabel = QtGui.QLabel()
        self.numberCombo = QtGui.QComboBox()
        self.createButton = QtGui.QPushButton()
        numberLayout = QtGui.QHBoxLayout()
        self.rotateLabel = QtGui.QLabel()
        self.watermarkRotate = QtGui.QSlider()
        self.rotateValue = QtGui.QDoubleSpinBox()
        rotateLayout = QtGui.QHBoxLayout()
        self.scaleLabel = QtGui.QLabel()
        self.watermarkScale = QtGui.QSlider()
        self.scaleValue = QtGui.QDoubleSpinBox()
        scaleLayout = QtGui.QHBoxLayout()
        self.opacityLabel = QtGui.QLabel()
        self.watermarkOpacity = QtGui.QSlider()
        self.opacityValue = QtGui.QDoubleSpinBox()
        opacityLayout = QtGui.QHBoxLayout()
        self.clipCombo = QtGui.QComboBox()
        self.startLabel = QtGui.QLabel()
        self.startFrame = QtGui.QLineEdit()
        self.endLabel = QtGui.QLabel()
        self.endFrame = QtGui.QLineEdit()
        self.renderButton = QtGui.QPushButton()


        #add widgets to layouts
        sourceLayout.addWidget(self.sourceLabel)
        sourceLayout.addWidget(self.sourcePath)
        sourceLayout.addWidget(self.sourceButton)
        formatLayout.addWidget(self.formatLabel)
        formatLayout.addWidget(self.formatCombo)
        formatLayout.addWidget(self.nameLabel)
        formatLayout.addWidget(self.formatName)
        formatLayout.addWidget(self.wLabel)
        formatLayout.addWidget(self.formatw)
        formatLayout.addWidget(self.hLabel)
        formatLayout.addWidget(self.formath)
        outputLayout.addWidget(self.outputLabel)
        outputLayout.addWidget(self.outputPath)
        outputLayout.addWidget(self.outputButton)
        typeLayout.addWidget(self.typeLabel)
        typeLayout.addWidget(self.typeCombo)
        typeLayout.setAlignment(QtCore.Qt.AlignLeft)
        textLayout.addWidget(self.textLabel)
        textLayout.addWidget(self.watermarkText)
        imageLayout.addWidget(self.imageLabel)
        imageLayout.addWidget(self.watermarkImage)
        imageLayout.addWidget(self.imageButton)
        numberLayout.addWidget(self.numberLabel)
        numberLayout.addWidget(self.numberCombo)
        numberLayout.addWidget(self.createButton)
        numberLayout.setAlignment(QtCore.Qt.AlignLeft)
        rotateLayout.addWidget(self.rotateLabel)
        rotateLayout.addWidget(self.watermarkRotate)
        rotateLayout.addWidget(self.rotateValue)
        scaleLayout.addWidget(self.scaleLabel)
        scaleLayout.addWidget(self.watermarkScale)
        scaleLayout.addWidget(self.scaleValue)
        opacityLayout.addWidget(self.opacityLabel)
        opacityLayout.addWidget(self.watermarkOpacity)
        opacityLayout.addWidget(self.opacityValue)
        renderRangeLayout.addWidget(self.clipCombo)
        renderRangeLayout.addWidget(self.startLabel)
        renderRangeLayout.addWidget(self.startFrame)
        renderRangeLayout.addWidget(self.endLabel)
        renderRangeLayout.addWidget(self.endFrame)

        #add layouts to tool panel
        self.layout().addLayout(sourceLayout)
        self.layout().addLayout(formatLayout)
        self.layout().addLayout(outputLayout)
        self.layout().addWidget(self.addclip)
        self.layout().addLayout(typeLayout)
        self.layout().addLayout(textLayout)
        self.layout().addLayout(imageLayout)
        self.layout().addLayout(numberLayout)
        self.layout().addLayout(rotateLayout)
        self.layout().addLayout(scaleLayout)
        self.layout().addLayout(opacityLayout)
        self.layout().addLayout(renderRangeLayout)
        self.layout().addWidget(self.renderButton)
        self.widgetSetup()

    def openClip(self):
        source = nuke.getClipname('Choose Source Clip')
        self.sourcePath.setText(source)

    def saveClip(self):
        output = nuke.getClipname('Choose Save Path')
        self.outputPath.setText(output)

    def openWatermark(self):
        imagePath = nuke.getFilename('Choose watermark Image','*.png *.exr *.tga *.tif *.tiff *.cin *.dpx')
        self.watermarkImage.setText(imagePath)

    def setOutputFormat(self,value): #change widgets editable or not
        if value == 'Custom':
            self.nameLabel.setEnabled(True)
            self.formatName.setEnabled(True)
            self.wLabel.setEnabled(True)
            self.formatw.setEnabled(True)
            self.hLabel.setEnabled(True)
            self.formath.setEnabled(True)
        else:
            self.nameLabel.setEnabled(False)
            self.formatName.setEnabled(False)
            self.wLabel.setEnabled(False)
            self.formatw.setEnabled(False)
            self.hLabel.setEnabled(False)
            self.formath.setEnabled(False)
            self.formatName.setText(nuke.formats()[self.formatCombo.currentIndex()].name())
            self.formatw.setText(str(nuke.formats()[self.formatCombo.currentIndex()].width()))
            self.formath.setText(str(nuke.formats()[self.formatCombo.currentIndex()].height()))

    def getExtention(self,fname):
        dot = fname.rfind('.')
        if dot == -1:
            return ''
        else:
            return fname[dot+1:]

    def createNodes(self): #create read,merge,reformat,write
        global flag
        if self.sourcePath.text() != '' and self.outputPath.text() != '':
            if self.getExtention(self.outputPath.text()) in filetypeList:
                #use custom format
                if self.formatCombo.currentText() == 'Custom':
                    if self.formatName.text()!='' and self.formatw.text()!='' and self.formath.text()!='':
                        try:
                            newWidth = int(self.formatw.text())
                            newHeight = int(self.formath.text())
                            if newWidth > 0 and newHeight > 0 and newWidth <= 8196 and newHeight <= 8196:
                                outputFormat = self.formatw.text()+' '+self.formath.text()+' '+self.formatName.text()
                                nuke.addFormat(outputFormat)
                                readNode = nuke.nodes.Read()
                                readNode['file'].fromUserText(self.sourcePath.text())
                                srcReadNodes.append(readNode)
                                watermarkMergeNode = nuke.nodes.Merge2()
                                watermarkMergeNode.setInput(0,readNode)
                                mergeNodes.append(watermarkMergeNode)
                                writeReformatNode = nuke.nodes.Reformat()
                                writeReformatNode.setInput(0,watermarkMergeNode)
                                writeReformatNode.knob('format').setValue(nuke.formats()[-1])
                                writeReformatNode.knob('black_outside').setValue(True) 
                                watermarkWriteNode = nuke.nodes.Write()
                                watermarkWriteNode.setInput(0,writeReformatNode)
                                watermarkWriteNode.knob('file').fromUserText(self.outputPath.text())
                                writeNodes.append(watermarkWriteNode)
                                nuke.toNode('Viewer1').setInput(flag,watermarkWriteNode)
                                flag = flag + 1
                                self.clipCombo.addItem('Clip '+str(flag))
                                self.clipCombo.setCurrentIndex(flag-1)
                                renderFirst.append(readNode.knob('first').value())
                                renderLast.append(readNode.knob('last').value())
                                self.startFrame.setText(str(readNode.knob('first').value()))
                                self.endFrame.setText(str(readNode.knob('last').value()))
                                self.sourcePath.clear()
                                self.outputPath.clear()
                                self.startFrame.clear()
                                self.endFrame.clear()
                            else:
                                nuke.message('should between 1-8196')
                        except ValueError:
                                nuke.message('width and height should be integer')
                    else:
                        nuke.message('should fill all information')
                #use standard format
                else:
                    readNode = nuke.nodes.Read()
                    readNode['file'].fromUserText(self.sourcePath.text())
                    srcReadNodes.append(readNode)
                    watermarkMergeNode = nuke.nodes.Merge2()
                    watermarkMergeNode.setInput(0,readNode)
                    mergeNodes.append(watermarkMergeNode)
                    writeReformatNode = nuke.nodes.Reformat()
                    writeReformatNode.setInput(0,watermarkMergeNode)
                    writeReformatNode.knob('format').setValue(nuke.formats()[self.formatCombo.currentIndex()])
                    writeReformatNode.knob('black_outside').setValue(True)             
                    watermarkWriteNode = nuke.nodes.Write()
                    watermarkWriteNode.setInput(0,writeReformatNode)
                    watermarkWriteNode.knob('file').fromUserText(self.outputPath.text())
                    writeNodes.append(watermarkWriteNode)
                    nuke.toNode('Viewer1').setInput(flag,watermarkWriteNode)
                    flag = flag + 1
                    self.clipCombo.addItem('Clip '+str(flag))
                    self.clipCombo.setCurrentIndex(flag-1)
                    renderFirst.append(readNode.knob('first').value())
                    renderLast.append(readNode.knob('last').value())
                    self.startFrame.setText(str(readNode.knob('first').value()))
                    self.endFrame.setText(str(readNode.knob('last').value()))
                    self.sourcePath.clear()
                    self.outputPath.clear()
            else:
                nuke.message('unknown output format')
        else:
            nuke.message('should set source and output')

    def typeChanged(self,value):
        if value == 'Text   ':
            self.textLabel.setEnabled(True)
            self.watermarkText.setEnabled(True)
            self.imageLabel.setEnabled(False)
            self.watermarkImage.setEnabled(False)
            self.imageButton.setEnabled(False)
        else:
            self.textLabel.setEnabled(False)
            self.watermarkText.setEnabled(False)
            self.imageLabel.setEnabled(True)
            self.watermarkImage.setEnabled(True)
            self.imageButton.setEnabled(True)

    def transformText(self,read,merge,text,num):
        #calculate 6 properties
        x1 = read.metadata('input/width')*(17.0/64.0)
        s1 = read.metadata('input/width')*(13.0/32.0)/600
        x2 = read.metadata('input/width')*(1.0/3.0)
        s2 = read.metadata('input/width')*((1.0/3.0)-(1.0/32.0))/600
        y1 = read.metadata('input/height')*(1.0/4.0)
        y2 = read.metadata('input/height')*(1.0/3.0)

        #set text node
        text.knob('box').setValue([0,0,read.metadata('input/width'),read.metadata('input/height')])
        text.knob('xjustify').setValue('center')
        text.knob('yjustify').setValue('center')

        #initialize transform node list
        del transformNodes[:]

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
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale')) #for storing s1/s2
                transform.knob('ori_scale').setValue(s1)
                transformNodes.append(transform)
                merge.setInput(i+3,transform)
            transformNodes[0].knob('translate').setValue([x1,0])  #watermark layout
            transformNodes[1].knob('translate').setValue([-x1,0])

        if num == 3:
            for i in range(3):
                transform = nuke.nodes.Transform()
                transform.setInput(0,text)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s2)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s2)
                transformNodes.append(transform)
                merge.setInput(i+3,transform)
            transformNodes[0].knob('translate').setValue([x2,0])
            transformNodes[1].knob('translate').setValue([-x2,0])

        if num == 4:
            for i in range(4):
                transform = nuke.nodes.Transform()
                transform.setInput(0,text)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s1)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s1)
                transformNodes.append(transform)
                merge.setInput(i+3,transform)
            transformNodes[0].knob('translate').setValue([x1,y1])
            transformNodes[1].knob('translate').setValue([-x1,y1])
            transformNodes[2].knob('translate').setValue([x1,-y1])
            transformNodes[3].knob('translate').setValue([-x1,-y1])

        if num == 6:
            for i in range(6):
                transform = nuke.nodes.Transform()
                transform.setInput(0,text)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s2)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s2)
                transformNodes.append(transform)
                merge.setInput(i+3,transform)
            transformNodes[0].knob('translate').setValue([x2,y1])
            transformNodes[1].knob('translate').setValue([-x2,y1])
            transformNodes[2].knob('translate').setValue([x2,-y1])
            transformNodes[3].knob('translate').setValue([-x2,-y1])
            transformNodes[4].knob('translate').setValue([0,-y1])
            transformNodes[5].knob('translate').setValue([0,y1])

        if num == 9:
            for i in range(9):
                transform = nuke.nodes.Transform()
                transform.setInput(0,text)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s2)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s2)
                transformNodes.append(transform)
                merge.setInput(i+3,transform)
            transformNodes[0].knob('translate').setValue([x2,y1])
            transformNodes[1].knob('translate').setValue([-x2,y1])
            transformNodes[2].knob('translate').setValue([x2,-y1])
            transformNodes[3].knob('translate').setValue([-x2,-y1])
            transformNodes[4].knob('translate').setValue([0,-y1])
            transformNodes[5].knob('translate').setValue([0,y1])
            transformNodes[6].knob('translate').setValue([x2,0])
            transformNodes[7].knob('translate').setValue([-x2,0])


    def transformImage(self,read,merge,image,position,num):
        x1 = read.metadata('input/width')*(17.0/64.0)
        s1 = read.metadata('input/width')*(13.0/32.0)/image.metadata('input/width')
        x2 = read.metadata('input/width')*(1.0/3.0)
        s2 = read.metadata('input/width')*((1.0/3.0)-(1.0/32.0))/image.metadata('input/width')
        y1 = read.metadata('input/height')*(1.0/4.0)
        y2 = read.metadata('input/height')*(1.0/3.0)
        position.knob('translate').setValue([read.metadata('input/width')/2-image.metadata('input/width')/2,read.metadata('input/height')/2-image.metadata('input/height')/2])
        del transformNodes[:]

        if num == 1:
            transform = nuke.nodes.Transform()
            transform.setInput(0,position)
            transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
            transform.knob('scale').setValue(0.5)
            transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
            transform.knob('ori_scale').setValue(0.5)
            merge.setInput(1,transform)

        if num == 2:
            for i in range(2):
                transform = nuke.nodes.Transform()
                transform.setInput(0,position)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s1)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s1)
                transformNodes.append(transform)
                merge.setInput(i+3,transform)
            transformNodes[0].knob('translate').setValue([x1,0])
            transformNodes[1].knob('translate').setValue([-x1,0])

        if num == 3:
            for i in range(3):
                transform = nuke.nodes.Transform()
                transform.setInput(0,position)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s2)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s2)
                transformNodes.append(transform)
                merge.setInput(i+3,transform)
            transformNodes[0].knob('translate').setValue([x2,0])
            transformNodes[1].knob('translate').setValue([-x2,0])

        if num == 4:
            for i in range(4):
                transform = nuke.nodes.Transform()
                transform.setInput(0,position)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s1)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s1)
                transformNodes.append(transform)
                merge.setInput(i+3,transform)
            transformNodes[0].knob('translate').setValue([x1,y1])
            transformNodes[1].knob('translate').setValue([-x1,y1])
            transformNodes[2].knob('translate').setValue([x1,-y1])
            transformNodes[3].knob('translate').setValue([-x1,-y1])

        if num == 6:
            for i in range(6):
                transform = nuke.nodes.Transform()
                transform.setInput(0,position)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s2)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s2)
                transformNodes.append(transform)
                merge.setInput(i+3,transform)
            transformNodes[0].knob('translate').setValue([x2,y1])
            transformNodes[1].knob('translate').setValue([-x2,y1])
            transformNodes[2].knob('translate').setValue([x2,-y1])
            transformNodes[3].knob('translate').setValue([-x2,-y1])
            transformNodes[4].knob('translate').setValue([0,-y1])
            transformNodes[5].knob('translate').setValue([0,y1])

        if num == 9:
            for i in range(9):
                transform = nuke.nodes.Transform()
                transform.setInput(0,position)
                transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
                transform.knob('scale').setValue(s2)
                transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))
                transform.knob('ori_scale').setValue(s2)
                transformNodes.append(transform)
                merge.setInput(i+3,transform)
            transformNodes[0].knob('translate').setValue([x2,y1])
            transformNodes[1].knob('translate').setValue([-x2,y1])
            transformNodes[2].knob('translate').setValue([x2,-y1])
            transformNodes[3].knob('translate').setValue([-x2,-y1])
            transformNodes[4].knob('translate').setValue([0,-y1])
            transformNodes[5].knob('translate').setValue([0,y1])
            transformNodes[6].knob('translate').setValue([x2,0])
            transformNodes[7].knob('translate').setValue([-x2,0])

    def watermarkTransform(self):
        for i in range(flag):
            read = srcReadNodes[i]
            merge = mergeNodes[i]
            num = int(self.numberCombo.currentText())
            if self.typeCombo.currentText() == 'Text   ' and self.watermarkText.text() != '':
                text = nuke.nodes.Text2()
                text.knob('message').setValue(self.watermarkText.text())
                self.transformText(read,merge,text,num)
            if self.typeCombo.currentText() == 'Image  ' and self.watermarkImage.text() != '':
                image = nuke.nodes.Read()
                image['file'].fromUserText(self.watermarkImage.text())
                imagePremultNode = nuke.nodes.Premult()
                imagePremultNode.setInput(0,image)
                position = nuke.nodes.Position()
                position.setInput(0,imagePremultNode)
                self.transformImage(read,merge,image,position,num)

    def realtimeTransform(self,s,v):  #realtime preview watermarks
        for i in nuke.allNodes():
            if i.Class() == 'Transform':
                if s == 'r':
                    i.knob('rotate').setValue(v)
                if s == 's':
                    i.knob('scale').setValue(i.knob('ori_scale').value()*v)
            if i.Class() == 'Merge2':
                if s == 'o':
                    i.knob('mix').setValue(v)

    #connect double_spin_box and slider
    def setRotateValue(self,value):
        self.rotateValue.setValue(value/100.0)
        self.realtimeTransform('r',self.rotateValue.value())
    def setScaleValue(self,value):
        self.scaleValue.setValue(value/100.0)
        self.realtimeTransform('s',self.scaleValue.value())
    def setOpacityValue(self,value):
        self.opacityValue.setValue(value/100.0)
        self.realtimeTransform('o',self.opacityValue.value()) 
    def setRotateSlider(self,value):
        self.watermarkRotate.setValue(value*100.0)
        self.realtimeTransform('r',value)
    def setScaleSlider(self,value):
        self.watermarkScale.setValue(value*100.0)
        self.realtimeTransform('s',value)
    def setOpacitySlider(self,value):
        self.watermarkOpacity.setValue(value*100.0)
        self.realtimeTransform('o',value)

    #setting custom rendering frame range
    def customStart(self,value):
        global renderFirst
        s = int(value)
        if srcReadNodes[self.clipCombo.currentIndex()].knob('first').value() <= s <= srcReadNodes[self.clipCombo.currentIndex()].knob('last').value():
            renderFirst[self.clipCombo.currentIndex()] = s

    def customEnd(self,value):
        global renderLast
        e = int(value)
        if srcReadNodes[self.clipCombo.currentIndex()].knob('first').value() <= e <= srcReadNodes[self.clipCombo.currentIndex()].knob('last').value() and int(self.startFrame.text()) <= e:
            renderLast[self.clipCombo.currentIndex()] = e

    #change current clip
    def renderRange(self):
        self.startFrame.setText(str(renderFirst[self.clipCombo.currentIndex()]))
        self.endFrame.setText(str(renderLast[self.clipCombo.currentIndex()]))

    def finalRendering(self): #rendering the results
        global flag
        for i in range(flag):
            nuke.execute(writeNodes[i].knob('name').value(),renderFirst[i],renderLast[i],1)
        del srcReadNodes[:]
        del mergeNodes[:]
        del writeNodes[:]
        del transformNodes[:]
        flag = 0

    def widgetSetup(self):
        #setup widgets
        self.sourceLabel.setText('Source:')
        self.sourceButton.setText('Open')
        self.startLabel.setText('first:')
        self.endLabel.setText('last:')
        self.formatLabel.setText('Format:')
        self.formatCombo.addItem('PC_Video')
        self.formatCombo.addItem('NTSC 720x486')
        self.formatCombo.addItem('PAL 720x576')
        self.formatCombo.addItem('NTSC_16:9')
        self.formatCombo.addItem('PAL_16:9')
        self.formatCombo.addItem('HD_720')
        self.formatCombo.addItem('HD_1080')
        self.formatCombo.addItem('UHD_4K')
        self.formatCombo.addItem('1K_Super35')
        self.formatCombo.addItem('1K_Cinemascope')
        self.formatCombo.addItem('2K_Super35')
        self.formatCombo.addItem('2K_Cinemascope')
        self.formatCombo.addItem('2K_DCP')
        self.formatCombo.addItem('4K_Super35')
        self.formatCombo.addItem('4K_Cinemascope')
        self.formatCombo.addItem('4K_DCP')
        self.formatCombo.addItem('square_256')
        self.formatCombo.addItem('square_512')
        self.formatCombo.addItem('square_1K')
        self.formatCombo.addItem('square_2K')
        self.formatCombo.setCurrentIndex(6)
        self.formatName.setText('HD_1080')
        self.formatw.setText('1920')
        self.formath.setText('1080')
        self.formatCombo.addItem('Custom')
        self.nameLabel.setText('name:')
        self.wLabel.setText('width')
        self.hLabel.setText('height')
        self.nameLabel.setEnabled(False)
        self.formatName.setEnabled(False)
        self.wLabel.setEnabled(False)
        self.formatw.setEnabled(False)
        self.hLabel.setEnabled(False)
        self.formath.setEnabled(False)
        self.outputLabel.setText('Output:')
        self.outputButton.setText('Save')
        self.addclip.setText('Add Clip')
        self.addclip.setMaximumWidth(100)
        self.typeLabel.setText('Type:')
        self.typeCombo.addItem('Text   ')
        self.typeCombo.addItem('Image  ')
        self.typeCombo.setMinimumWidth(60)
        self.textLabel.setText('Text:')
        self.imageLabel.setText('Image:')
        self.imageButton.setText('Open')
        self.imageLabel.setEnabled(False)
        self.watermarkImage.setEnabled(False)
        self.imageButton.setEnabled(False)
        self.numberLabel.setText('Number:')
        self.numberCombo.addItem('1')
        self.numberCombo.addItem('2')
        self.numberCombo.addItem('3')
        self.numberCombo.addItem('4')
        self.numberCombo.addItem('6')
        self.numberCombo.addItem('9')
        self.numberCombo.setMinimumWidth(50)
        self.createButton.setText('Create')
        self.rotateLabel.setText('Rotate:')
        self.watermarkRotate.setRange(-18000,18000)
        self.watermarkRotate.setOrientation(QtCore.Qt.Horizontal)
        self.watermarkRotate.setTickPosition(QtGui.QSlider.TicksBelow)
        self.watermarkRotate.setTickInterval(2000)
        self.rotateValue.setRange(-180.00,180.00)
        self.scaleLabel.setText('Scale:')
        self.watermarkScale.setRange(30,150)
        self.watermarkScale.setOrientation(QtCore.Qt.Horizontal)
        self.watermarkScale.setTickPosition(QtGui.QSlider.TicksBelow)
        self.watermarkScale.setTickInterval(10)
        self.scaleValue.setRange(0.30,1.50)
        self.opacityLabel.setText('Opacity:')
        self.watermarkOpacity.setRange(0,100)
        self.watermarkOpacity.setOrientation(QtCore.Qt.Horizontal)
        self.watermarkOpacity.setTickPosition(QtGui.QSlider.TicksBelow)
        self.watermarkOpacity.setTickInterval(10)
        self.opacityValue.setRange(0.00,1.00)
        self.watermarkScale.setValue(100)
        self.watermarkOpacity.setValue(100)
        self.scaleValue.setValue(1.00)
        self.opacityValue.setValue(1.00)
        self.rotateValue.setSingleStep(1.00)
        self.scaleValue.setSingleStep(0.05)
        self.opacityValue.setSingleStep(0.05)
        self.renderButton.setText('Render')
        self.renderButton.setMaximumWidth(100)

        #connect signal and slot
        self.sourceButton.clicked.connect(self.openClip)
        self.formatCombo.activated[str].connect(self.setOutputFormat)
        self.typeCombo.activated[str].connect(self.typeChanged)
        self.watermarkRotate.valueChanged.connect(self.setRotateValue)
        self.watermarkScale.valueChanged.connect(self.setScaleValue)
        self.watermarkOpacity.valueChanged.connect(self.setOpacityValue)
        self.rotateValue.valueChanged.connect(self.setRotateSlider)
        self.scaleValue.valueChanged.connect(self.setScaleSlider)
        self.opacityValue.valueChanged.connect(self.setOpacitySlider)
        self.outputButton.clicked.connect(self.saveClip)
        self.addclip.clicked.connect(self.createNodes)
        self.imageButton.clicked.connect(self.openWatermark)
        self.createButton.clicked.connect(self.watermarkTransform)
        self.clipCombo.activated[str].connect(self.renderRange)
        self.renderButton.clicked.connect(self.finalRendering)
        self.startFrame.textEdited.connect(self.customStart)
        self.endFrame.textEdited.connect(self.customEnd)

def showTools():
    pane = nuke.getPaneFor('Properties.1')
    panels.registerWidgetAsPanel('WatermarkControlPanel', 'Watermark Tools', 'uk.co.thefoundry.WatermarkControlPanel', True).addToPane(pane)

nuke.menu('Nodes').addCommand('CustomCommands/WatermarkTools', showTools )