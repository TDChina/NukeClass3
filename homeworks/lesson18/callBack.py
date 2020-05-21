# _*_ coding: utf-8 _*_
# @Time      : 5/19/2020 10:57 PM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : callBack.py
# @software  : PyCharm

import os
import re

def get_nukepro_path():
    nukeFilePath = nuke.root().name()
    print(nukeFilePath)
    if nukeFilePath == 'Root':
        nuke.message('Project file not saved')
        return 0
    parent_folder = os.path.splitext(nukeFilePath)[0]
    fileName = os.path.basename(parent_folder)
    nukePro_version = re.search(r"(?i)v\d*", fileName, re.M|re.I).group()
    if nukePro_version:
        return parent_folder,nukePro_version,fileName
    else:
        nuke.message('Project name does not identify version name')
        return 0


def setWriteFile():
    writeNode = nuke.thisNode()

    projectPath = get_nukepro_path()
    if not projectPath:
        return 0
    writeNode.knob('file').fromUserText(projectPath[0]+"/%s.mov" %projectPath[2])
    writeNode.knob('beforeRender').setValue('export_decide()')
    writeNode.knob('afterRender').setValue('set_up_version()')

def set_up_version():
    nukescripts.version_up()
    nukescripts.script_version_up()

def export_decide():
    writeNode = nuke.thisNode()
    exportPath = writeNode.knob('file').value()
    print(exportPath)
    if not writeNode.inputs():
        nuke.message('Input node is empty')
        # 执行终止异常
        raise RuntimeError('Input node is empty')

    if os.path.exists(os.path.split(exportPath)[0]):
        if not nuke.ask('File already exists, overwrite or not'):
            raise RuntimeError('Cancel rendering')
    else:
        os.mkdir(os.path.split(exportPath)[0])


nuke.addOnUserCreate(setWriteFile, nodeClass = 'Write')

nuke.removeOnUserCreate(setWriteFile, nodeClass = 'Write')



