import nuke
nuke.scriptSource('E:/Nuke_mylself/Nuke_Dev_test/test_01.nk')
buttom_node = None
for node in nuke.allNodes():
    if node.Class() != 'Viewer':
        if buttom_node is None:
            buttom_node = node
        if node.ypos() > buttom_node.ypos():
            buttom_node = node
print buttom_node.name()
buttom_node.setSelected(True)
new_node = nuke.createNode('Merge')
new_node.setXYpos(buttom_node.xpos()-new_node.screenWidth()/2+buttom_node.screenWidth()/2, buttom_node.ypos() + 50 )
print nuke.allNodes()
nuke.scriptSource('E:/Nuke_mylself/Nuke_Dev_test/test_02.nk')
print nuke.allNodes()
new_node.setInput(0, nuke.toNode('Dot38'))
nuke.scriptSource('E:/Nuke_mylself/Nuke_Dev_test/test_03.nk')
nuke.toNode('Dot8').setInput(0, nuke.toNode('Dot38'))
new_node.setInput(0, nuke.toNode('Dot28'))

nuke.scriptSaveAs('E:/Nuke_mylself/Nuke_Dev_test/test_04.nk')