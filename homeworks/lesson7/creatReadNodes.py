# -*- coding: utf-8 -*-
import os
import nuke
basePath = r"X:/PET/shot_work/s074/c0002/lgt/img/"
def file_name(file_dir):
    finalFilePath = []
    if  os.path.exists(file_dir):
        for root, dirs, files in os.walk(file_dir):
            #print(root)
            #print nuke.getFileNameList(root)
            for num in nuke.getFileNameList(root):
                #print root.replace('\\','/') +'/'+ num
                if not os.path.isdir(root.replace('\\','/') +'/'+ num) :
                    #print root.replace('\\','/') +'/'+ num
                    finalFilePath.append(root.replace('\\','/') +'/'+ num)
    return finalFilePath
def creatReadNode()
    temp = file_name(basePath)
    for p in temp:
        readNode = nuke.createNode('Read')
        readNode.knob('file').fromUserText(p)
creatReadNode()