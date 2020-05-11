# _*_ coding: utf-8 _*_
# @Time      : 4/28/2020 10:32 PM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : switch.py
# @software  : PyCharm

def layoutNode(selecteNode, node):
    node['xpos'].setValue(selecteNode.xpos() + selecteNode.screenWidth() / 2 - node.screenWidth() / 2)
    node['ypos'].setValue(selecteNode.ypos() + 120)


def createNode(node, selecteNode, x, y = 0):
    node['xpos'].setValue(selecteNode.xpos() - x)
    node['ypos'].setValue(selecteNode.ypos() + y)


def switchImages():
    node = nuke.thisNode()
    MatteCh = node['Switch'].value()
    if MatteCh == "Original":
        nuke.toNode("MCHswitch_temp").knob("which").setValue(1)
        return 0
    if MatteCh == "Alpha":
        nuke.toNode("MCHswitch_temp").knob("which").setValue(0)
        return 0
    if MatteCh == "Checkboard":
        nuke.toNode("MCHMerge_temp").setInput(0, nuke.toNode("MCHCheckerBoard_temp"))
        nuke.toNode("MCHswitch_temp").knob("which").setValue(2)
        return 0
    if MatteCh == "background":
        nuke.toNode("MCHMerge_temp").setInput(0, nuke.toNode("MCHreformat_temp"))
        nuke.toNode("MCHswitch_temp").knob("which").setValue(2)
        return 0
    if MatteCh == "CustomColor":
        nuke.toNode("MCHMerge_temp").setInput(0, nuke.toNode("MCHConstant_temp"))
        nuke.toNode("MCHswitch_temp").knob("which").setValue(2)
        return 0


def main():
    if nuke.selectedNode().Class() in ('Read'):
        selecteNode = nuke.selectedNode()
        dot = nuke.createNode("Dot", 'name "MCHDot_temp"', inpanel = False)
        layoutNode(selecteNode, dot)
        shuffle = nuke.createNode("Shuffle", 'name "MCHshuffle_temp"', inpanel = False)
        layoutNode(dot, shuffle)
        shuffle.knob("red").setValue("alpha")
        shuffle.knob("blue").setValue("alpha")
        shuffle.knob("green").setValue("alpha")
        switch = nuke.createNode("Switch", 'name "MCHswitch_temp"', inpanel = False)
        layoutNode(shuffle, switch)
        switch['xpos'].setValue(switch.xpos() - 150)
        switch.setInput(1, dot)
        switch.knob("which").setValue(1)
        constant = nuke.nodes.Constant(name = 'MCHConstant_temp')
        createNode(constant, selecteNode, 150)
        check = nuke.nodes.CheckerBoard2(name = 'MCHCheckerBoard_temp')
        createNode(check, selecteNode, 250)
        premult = nuke.nodes.Premult(name = 'MCHPremult_temp')
        createNode(premult, selecteNode, 150, 150)
        merge = nuke.nodes.Merge2(name = 'MCHMerge_temp')
        createNode(merge, selecteNode, 250, 250)
        background = nuke.nodes.Read(name = 'MCHbackground_temp')
        createNode(background, selecteNode, 350)

        reformat = nuke.nodes.Reformat(name = 'MCHreformat_temp')
        createNode(reformat, selecteNode, 350, 100)

        reformat.setInput(0, background)
        reformat.knob("format").fromScript('{{%s.format}}' % selecteNode.knob('name').value())

        premult.setInput(0, dot)
        merge.setInput(1, premult)
        switch.setInput(2, merge)
        merge.setInput(0, constant)
        nuke.toNode("Viewer1").setInput(0, switch)
        constant.knob("format").fromScript('{{%s.format}}' % selecteNode.knob('name').value())
        check.knob("format").fromScript('{{%s.format}}' % selecteNode.knob('name').value())

        MatteCh = nuke.thisNode()
        constant.knob("color").fromScript('{{%s.BGcolor}}' %MatteCh.knob('name').value())
        if MatteCh.knob("background").value()=="":
            nuke.message("Background image is not specified")
        else:
            background.knob('file').fromUserText(MatteCh.knob('background').value())

    else:
        nuke.message("Please select at least one Read node")


def updataMC():
    if not nuke.toNode("MCHDot_temp"):
        if nuke.nodesSelected():
            main()
        else:
            nuke.message("Please select at least one Read node")

    else:
        switchImages()


updataMC()



allNode = ["MCHswitch_temp",'MCHMerge_temp','MCHDot_temp','MCHConstant_temp','MCHPremult_temp','MCHCheckerBoard_temp','MCHreformat_temp','MCHbackground_temp','MCHshuffle_temp']
def removeNode():
    if nuke.toNode("MCHMerge_temp"):
        for i in allNode:
            nuke.delete(nuke.toNode("%s" %i))






