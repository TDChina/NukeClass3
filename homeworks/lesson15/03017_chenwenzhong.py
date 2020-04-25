import nuke
import os


def mattechecker():
    # create NoOp node
    noop_node = nuke.createNode('NoOp')

    # the layers 
    layers_knob = nuke.Enumeration_Knob('layers', 'Layers', ["Source", "Key", 'Constant', 'Checkboard', 'BackGround'])

    # create PyScript_Knob
    python_knob = nuke.PyScript_Knob('get_slate', 'Get_slate', """

slate = nuke.menu('Nodes').menu('ToolSets').findItem('Check').invoke()
check_node = nuke.thisNode()
nodes = nuke.selectedNodes()
for node in nodes:
    if node.Class() == 'Switch':
        node['which'].setExpression(check_node.name()+'.'+check_node['layers'].name())
        nuke.thisNode().setInput(0, node)
        nuke.thisNode().setXYpos(node.xpos(), node.ypos()+100)
    if node.Class() == 'Constant':
        node['color'].setExpression(check_node.name()+'.'+check_node['constant_color'].name())

    if node.Class() == 'Read':
        if node.name().find('Alpha')==0:
            alpha_path = check_node['alpha_path'].value()
            full_list = alpha_path.split('/')
            folder = ('/').join(full_list[:-1])
            seq_path = nuke.getFileNameList(folder)
            node['file'].fromUserText(folder + '/' + seq_path[0])


        if node.name().find('Material')==0:
            material_path = check_node['material_path'].value()
            full_list = material_path.split('/')
            folder = ('/').join(full_list[:-1])
            seq_path = nuke.getFileNameList(folder)
            node['file'].fromUserText(folder + '/' + seq_path[0])


        if node.name().find('BackGround')==0:
            background_path = check_node['background_path'].value()
            full_list = background_path.split('/')
            folder = ('/').join(full_list[:-1])
            seq_path = nuke.getFileNameList(folder)
            node['file'].fromUserText(folder + '/' + seq_path[0])
    """)

    # create Knobs
    file_knob = nuke.File_Knob('material_path', 'Material_path')
    alpha_knob = nuke.File_Knob('alpha_path', 'Alpha_path')
    background_knob = nuke.File_Knob('background_path', 'Background_path')

    constant_color = nuke.AColor_Knob('constant_color', 'Constant_color')


    # add knobs
    noop_node.addKnob(layers_knob)
    noop_node.addKnob(python_knob)
    noop_node.addKnob(file_knob)
    noop_node.addKnob(alpha_knob)
    noop_node.addKnob(background_knob)
    noop_node.addKnob(constant_color)

mattechecker()
