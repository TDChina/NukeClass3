# _*_ coding: utf-8 _*_
# @Time      : 5/30/2020 2:25 PM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : readPath.py
# @software  : PyCharm

import os
import shutil
import threading

projectServerPath = '//ZUOKANGBO/work/test/temp'


def getReadList():
    nodeList = nuke.allNodes()
    listRead = []
    for i in nodeList:
        if i.Class() == 'Read':
            listRead.append(i)
    return listRead


def pathNet():
    listRead = getReadList()
    for i in listRead:
        readPath = i['file'].value()
        pathNet = isNetPath(readPath)
        if not pathNet:
            copyFile(readPath, i)

def copyFile(filePath, readNode):
    sourcePath = os.path.dirname(filePath)
    ServerPath = os.path.join(projectServerPath, os.path.basename(sourcePath))
    if not os.path.exists(ServerPath):
        os.makedirs(ServerPath)
    for root, dirs, files in os.walk(sourcePath):
        for file in files:
            src_file = os.path.join(root, file)
            shutil.copy(src_file, ServerPath)
    baseName = os.path.basename(sourcePath) + '/' + os.path.basename(filePath)
    readNode['file'].setValue(projectServerPath + '/%s' % baseName)

def replacePath(readNode, baseName):
    readNode['file'].setValue(projectServerPath + '/%s' % baseName)


def isNetPath(path):
    if path.startswith(projectServerPath):
        return True
    else:
        return False

threading.Thread(target = pathNet).start()
