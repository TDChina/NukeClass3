# _*_ coding: utf-8 _*_
# @Time      : 4/24/2020 10:41 PM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : exportVideo.py
# @software  : PyCharm

import os

def exportVideo():

    sequPath = nuke.getClipname('get file')
    readNode = nuke.createNode('Read',inpanel = False)
    readNode.knob('file').fromUserText(sequPath)
    reformat = nuke.createNode('Reformat',inpanel = False)['format']
    nuke.addFormat('1280 720 export')
    reformat.setValue('export')
    write = nuke.createNode('Write',inpanel = False)
    write.knob('file').fromUserText(os.path.dirname(sequPath)+"test.mov")
    write.knob('meta_codec').setValue("avc1")
    write.knob('mov32_fps').setValue(24.0)
    nuke.render(write, readNode.knob('first').value(), readNode.knob('last').value(), 1)

if __name__ == '__main__':
    exportVideo()

