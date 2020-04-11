import nuke

check_node = nuke.toNode('CheckerBoard3')
blur_node = nuke.toNode('Blur3')
check_node.setXYpos(check_node.xpos(), check_node.ypos()-300)
blur_node.setXYpos(blur_node.xpos(), blur_node.ypos()-300)

dot = nuke.toNode('Dot4')
dot.setInput(0, blur_node)

merge_node = nuke.toNode('Merge5')
merge_node1 = nuke.toNode('Merge6')
merge_node.setInput(0, merge_node1)

grade_node = nuke.toNode('Grade6')

grade_node.setXpos(merge_node.xpos())
merge_node1.setXpos(merge_node.xpos())
dot.setXpos(merge_node.xpos()+merge_node.screenWidth()/2-dot.screenWidth()/2)


cc_node = nuke.toNode('ColorCorrect3')
cc_node.setXYpos(dot.xpos()+100, dot.ypos()-dot.screenHeight()/2)
cc_node.setSelected(True)
dot1 = nuke.createNode('Dot')
dot1.setYpos(merge_node1.ypos()+dot1.screenHeight()/2)