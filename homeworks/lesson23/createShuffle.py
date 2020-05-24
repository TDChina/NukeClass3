# _*_ coding: utf-8 _*_
# @Time      : 5/24/2020 7:23 PM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : createShuffle.py
# @software  : PyCharm

def shuffle_exr():
    selectNode =nuke.selectedNode()
    laList=[]
    channelsList = selectNode.channels()
    for i in channelsList:
        temp_chan = i.split('.')
        if (len(laList)) == 0:
            laList.append(temp_chan[0])
        elif laList[-1]!=temp_chan[0]:
                laList.append(temp_chan[0])
    dotNodt = nuke.createNode('Dot')
    for i in laList:
        creteShuffle = nuke.nodes.Shuffle(name=i)
        creteShuffle.setInput(0, dotNodt)
        creteShuffle['in'].setValue(i)

if __name__ == '__main__':
    shuffle_exr()
