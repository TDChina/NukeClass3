#coding:utf-8
import nuke
def H_render():
    path1 = 'F:\\ff\\sucai\\'
    sequence_name = 'xuehua1'
    nuke.getFileNameList(path1)
    for i in nuke.getFileNameList(path1):
        if i == sequence_name:
            path1 = 'F:\\ff\\sucai\\xuehua1\\'
            for ii in nuke.getFileNameList(path1):
                node = nuke.createNode('Read', inpanel=False)
                node.knob('file').fromUserText(path1 + ii)
        else:
            node = nuke.createNode('Read', inpanel=False)
            node.knob('file').fromUserText(path1 + i)