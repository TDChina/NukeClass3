import nuke
import sys,os

#initialize lists for storing nodes
srcReadNodes = []
mergeNodes = []
writeNodes = []
transformNodes = []

#flag is the number of source clips
flag = 0

outputFormat = ''
renderFirst = []
renderLast = []

#legal output file extention
filetypeList = ['cin', 'dpx','exr','fpi','hdr','jpg','jpeg','mov','mp4','null','pic','png','sgi','tga','tiff','tif','xpm','yuv']

def settingFormat(width,height):
    global outputFormat
    for i in nuke.formats():
        if width == i.width() and height == i.height():
            outputFormat = i
            return True
    return False

def getExtention(fname):
        dot = fname.rfind('.')
        if dot == -1:
            return ''
        else:
            return fname[dot+1:]

def createNodes(source,w,h,output): #create read,merge,reformat,write
    global outputFormat
    global flag
    if source != '' and output != '':
        if getExtention(output) in filetypeList:
            r = nuke.nodes.Read()
            r.knob('file').fromUserText(source)
            srcReadNodes.append(r)
            m = nuke.nodes.Merge2()
            m.setInput(0,r)
            mergeNodes.append(m)
            if not settingFormat(w,h):  #create new format
                if 0<w<=8192 and 0<h<=8192:
                    outputFormat = str(w)+' '+str(h)+' '+'newformat'
                    nuke.addFormat(outputFormat)
                    f = nuke.nodes.Reformat()
                    f.setInput(0,m)
                    f.knob('black_outside').setValue(True)
                    f.knob('format').setValue(nuke.formats()[-1])
                else:
                    'illegal format'
            else:
                f = nuke.nodes.Reformat()
                f.setInput(0,m)
                f.knob('black_outside').setValue(True)
                f.knob('format').setValue(outputFormat)
            w = nuke.nodes.Write()
            w.knob('file').fromUserText(outputPath)
            w.setInput(0,f)
            writeNodes.append(w)
            flag = flag + 1
        else:
            print 'unknown output format'
    else:
        print 'please fill all information'

def transformText(read,merge,text,position,num):
    #calculate 6 properties
    x1 = read.metadata('input/width')*(17.0/64.0)
    s1 = read.metadata('input/width')*(13.0/32.0)/600
    x2 = read.metadata('input/width')*(1.0/3.0)
    s2 = read.metadata('input/width')*((1.0/3.0)-(1.0/32.0))/600
    y1 = read.metadata('input/height')*(1.0/4.0)
    y2 = read.metadata('input/height')*(1.0/3.0)

    #set text node
    text.knob('box').setValue([0,0,600,200])
    text.knob('xjustify').setValue('center')
    text.knob('yjustify').setValue('center')
    position.knob('translate').setValue([read.metadata('input/width')/2-300,read.metadata('input/height')/2-100])
    
    #initialize transform node list
    del transformNodes[:]

    if num not in [1,2,3,4,6,9]:
        print 'wrong number'
        return

    if num == 1:
        transform = nuke.nodes.Transform()
        transform.setInput(0,position)
        transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
        transform.knob('scale').setValue(s1*2)
        transform.addKnob(nuke.Double_Knob('ori_scale','original scale')) 
        transform.knob('ori_scale').setValue(s1*2)
        merge.setInput(1,transform)

    if num == 2:
        for i in range(2):
            transform = nuke.nodes.Transform()
            transform.setInput(0,position)
            transform.knob('center').setValue([(read.metadata('input/width')/2),(read.metadata('input/height')/2)])
            transform.knob('scale').setValue(s1)
            transform.addKnob(nuke.Double_Knob('ori_scale','original scale'))  #for storing s1/s2
            transform.knob('ori_scale').setValue(s1)
            transformNodes.append(transform)
            merge.setInput(i+3,transform)
        transformNodes[0].knob('translate').setValue([x1,0])  #watermark layout
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


def transformImage(read,merge,image,position,num):
    x1 = read.metadata('input/width')*(17.0/64.0)
    s1 = read.metadata('input/width')*(13.0/32.0)/image.metadata('input/width')
    x2 = read.metadata('input/width')*(1.0/3.0)
    s2 = read.metadata('input/width')*((1.0/3.0)-(1.0/32.0))/image.metadata('input/width')
    y1 = read.metadata('input/height')*(1.0/4.0)
    y2 = read.metadata('input/height')*(1.0/3.0)
    position.knob('translate').setValue([read.metadata('input/width')/2-image.metadata('input/width')/2,read.metadata('input/height')/2-image.metadata('input/height')/2])
    del transformNodes[:]

    if num not in [1,2,3,4,6,9]:
        print 'wrong number'
        return

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

def watermarkTransform(watermarkType,watermark,num):
    for i in range(flag):
        read = srcReadNodes[i]
        merge = mergeNodes[i]
        if watermarkType == 'text' and watermark != '':
            text = nuke.nodes.Text2()
            text.knob('message').setValue(watermark)
            position = nuke.nodes.Position()
            position.setInput(0,text)
            transformText(read,merge,text,position,num)
        elif watermarkType == 'image' and watermark != '':
            image = nuke.nodes.Read()
            image['file'].fromUserText(watermark)
            imagePremultNode = nuke.nodes.Premult()
            imagePremultNode.setInput(0,image)
            position = nuke.nodes.Position()
            position.setInput(0,imagePremultNode)
            transformImage(read,merge,image,position,num)
        else:
            print 'wrong type or incomplete information'

def finalRendering():
    global flag
    for i in range(flag):
        if renderFirst[i]==0 and renderLast[i]==0:
            nuke.render(writeNodes[i].knob('name').value(),srcReadNodes[i].knob('first').value(),srcReadNodes[i].knob('last').value(),1)
        elif srcReadNodes[i].knob('first').value()<=renderFirst[i] and 0<renderLast[i] <=srcReadNodes[i].knob('last').value() and renderFirst[i] <= renderLast[i]:
            nuke.render(writeNodes[i].knob('name').value(),renderFirst[i],renderLast[i],1)
        else:
            print 'illegal frame range'
    del srcReadNodes[:] #source files
    del mergeNodes[:]   #merge nodes attached to source files
    del writeNodes[:]   #write nodes
    del transformNodes[:] #transform nodes of multiple watermark
    flag = 0

def delEndLine(s):
    if s.rfind('\n') == -1:
        return s
    else:
        return s[:s.rfind('\n')]

opacity =  float(sys.argv[-1][1:])
scale =  float(sys.argv[-2][1:])
rotate =  float(sys.argv[-3][1:])
number =  int(sys.argv[-4][1:])
content = sys.argv[-5]
wmType = sys.argv[-6]

tempList = sys.argv

if getExtention(tempList[1]) == 'txt':
    f = open(tempList[1],'r')
    sys.argv.remove(tempList[1])
    for line in f:
        sys.argv.insert(1,delEndLine(line))

for i in range(len(sys.argv)-7):
    clipSetting = sys.argv[-(7+i)].split(',')
    sourcePath =  clipSetting[0]
    outputPath = clipSetting[3]
    renderFirst.append(int(clipSetting[4]))
    renderLast.append(int(clipSetting[5]))
    try:
        formatw = int(clipSetting[1])
        formath = int(clipSetting[2])
        createNodes(sourcePath,formatw,formath,outputPath)
        watermarkTransform(wmType,content,number)
    except ValueError:
        print 'format width/height should be integer'

if -180<=rotate<=180 and 0.3<=scale<=1.5 and 0<=opacity<=1:
    for i in nuke.allNodes():
        if i.Class() == 'Transform':
            i.knob('rotate').setValue(rotate)
            i.knob('scale').setValue(i.knob('ori_scale').value()*scale)
        if i.Class() == 'Merge2':
            i.knob('mix').setValue(opacity)
else:
    print 'properties out of range'


finalRendering()
