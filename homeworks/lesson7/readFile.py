# _*_ coding: utf-8 _*_
# @Time      : 4/11/2020 11:58 PM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : readFile.py
# @software  : PyCharm
import os


def fileFormatList():
    '''File format to import'''

    p = nuke.Panel('File format to import')
    p.addSingleLineInput('Formats', '.bmp,.exr,.png,.jpg,.jpeg,.tga,.tif,.tiff')
    p.show()
    fileFormatSl = p.value('Formats').split(',')
    if len(fileFormatSl) !=0:
        return tuple(fileFormatSl)
    else:
        nuke.message("Wrong input path")
        return False

def readFiles():
    '''Accept a path list'''
    inputPathList = getInputPath()
    fileFormatSl = fileFormatList()

    for rootdir in inputPathList:
        getFilePathList = getFilePath(rootdir,fileFormatSl)
        if getFilePathList:
            for readPathName in getFilePathList:
                readNode = nuke.nodes.Read().knob('file').fromUserText(readPathName)

def getFilePath(rootdir,fileFormatSl):
    ''' get file full path'''
    if os.path.exists(rootdir):
        fileFullPathList = []
        singleFileList = []
        fileNameList = nuke.getFileNameList(rootdir, False, True, False)
        for filename in fileNameList:
            fileFormat = filename.split('#')
            if len(fileFormat)>1:
                if fileFormat[-1].startswith(fileFormatSl):
                    frameEnd = fileFormat[-1].split('-')
                    frameCount = len(str(frameEnd[-1]))
                    fullPath = os.path.join(rootdir,fileFormat[0] + r'%' + '%sd' %frameCount + fileFormat[-1])
                    fileFullPathList.append(fullPath)
            else:
                if filename.endswith(fileFormatSl):
                    singleFileList.append(os.path.join(rootdir,filename))

        return fileFullPathList + singleFileList
    else:
        return False

def getInputPath():
    '''Get user input path list'''
    inputPath = nuke.getInput('Please enter the path', 'Multiple separated by ","')
    if len(inputPath)>3 and inputPath != 'Multiple separated by ","':
        inputPathList = inputPath.split(',')
        return inputPathList
    else:
        nuke.message("Wrong input path")
        return False

if __name__=='__main__':
    readFiles()