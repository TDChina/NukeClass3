# _*_ coding: utf-8 _*_
# @Time      : 4/15/2020 9:29 PM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : import_nk.py
# @software  : PyCharm

import os

import nodeLayout

def getNukeFileLists(path):
    '''get nuke name path'''
    if os.path.exists(path):
        nukeFileList = []
        dirFilst = os.listdir(path)
        for fileName in dirFilst:
            if os.path.isfile(os.path.join(path,fileName)):
                fileFormat = fileName.split('.')
                if fileFormat[-1].endswith(("nk")):
                    nukeFileList.append(os.path.join(path,fileName))
        print(nukeFileList)
        return nukeFileList
    else:
        print("input path name error")
        return False


def import_node():
    path = raw_input("input nuke file path:\n")
    getNukeFileList = getNukeFileLists(path)
    for nukeFile in getNukeFileList:
        nuke.scriptReadFile(nukeFile)

    nodeLayout.main()
    saveNekuFile(path)

def saveNekuFile(path):
    fileName = raw_input('input new file save name:\n')
    newName = os.path.join(path, fileName)
    if os.path.isfile(newName):
        print('The name you entered already exists')
    else:
        if newName.endswith(('.nk')):
            nuke.scriptSaveAs(newName)
        else:
            nuke.scriptSaveAs(newName+".nk")

import_node()