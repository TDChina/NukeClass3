# _*_ coding: utf-8 _*_
# @Time      : 4/13/2020 10:30 PM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : nodeLayout.py
# @software  : PyCharm


def toNode(node):
    getNode = nuke.toNode('%s' % node)
    return getNode

def linkNode():
    toNode('Merge1').setInput(1, toNode('Merge2'))
    toNode('Dot1').setInput(0, toNode('ColorBars1'))

def moveNode(node, count, axis):
    if axis == 'y':
        toNode('%s' % node).setYpos(toNode("Merge1").ypos() - int('%d' % count))
    if axis == 'x':
        toNode('%s' % node).setXpos(toNode("Merge1").xpos() - int('%d' % count))

def getNodeCen(node):
    colorBarslX = toNode("%s" % node).xpos() + toNode("%s" % node).screenWidth() / 2
    return colorBarslX

def getNodeCenY(node):
    colorBarsly = toNode("%s" % node).ypos() + toNode("%s" % node).screenHeight() / 2
    return colorBarsly

def setYpos(node, pos):
    return node.setYpos(pos - node.screenHeight() / 2)

def main():
    linkNode()
    moveNode("Constant1", 300, 'y')
    moveNode("Text1", 290 - toNode("Constant1").screenHeight(), 'y')
    moveNode("Constant1", 300, 'x')
    moveNode("Text1", 300, 'x')
    moveNode("Transform1", 300, 'x')

    moveNode("ColorBars1", 350, 'y')
    moveNode("ColorBars1", -200, 'x')

    colorBarslY = toNode("ColorBars1").ypos() + toNode("ColorBars1").screenHeight()
    toNode("Dot1").setXYpos(getNodeCen("ColorBars1") - toNode("Dot1").screenWidth() / 2, colorBarslY + 50)

    toNode("Merge2").setXYpos(toNode("Merge1").xpos(), toNode("Merge1").ypos() - 150)
    toNode("Glow1").setXYpos(toNode("Merge1").xpos(), getNodeCenY("Dot1") - toNode("Glow1").screenHeight() / 2)

    toNode("ColorCorrect1").setYpos(toNode("Glow1").ypos())
    toNode("ColorCorrect1").setXpos(toNode("Glow1").xpos()+400)

    toNode("ColorCorrect1").selectOnly()
    dot2 = nuke.createNode('Dot', inpanel = False)
    setYpos(dot2, toNode("Merge2").ypos() + toNode("Merge2").screenHeight() / 2)

if __name__ == "__main__":
    main()
