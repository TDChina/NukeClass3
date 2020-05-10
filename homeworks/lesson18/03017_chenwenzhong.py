import os
import re
import nuke


def create_write_dir():
    node = nuke.thisNode()
    full_path = nuke.scriptName()
    filename = full_path.split('.')[0]
    split_path = filename.split('/')
    project_folder = split_path[-2]
    output_folder = re.sub(project_folder, 'output', filename) + '/'
    node['file'].setValue(output_folder)


def before_render():
    filename = nuke.thisNode()['file'].value()
    dir_path = os.path.dirname(filename)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def write_version_up():
    script_name = nuke.scriptName()
    filename = nuke.thisNode()['file'].value()
    pattern = re.compile('[vV][0-9]+')
    old_version = re.search(pattern, filename).group()
    new_version = re.search(pattern, script_name).group()
    replace_version = re.sub(old_version, new_version, filename)
    nuke.thisNode()['file'].setValue(replace_version)


def create_read_from_write():
    """
    create a read node from a selected write node
    :return: None
    """
    selected_node = nuke.thisNode()
    if selected_node.Class() == 'Write':
        node = nuke.createNode('Read')
        node.setXpos(int(selected_node['xpos'].getValue()))
        node.setYpos(int(selected_node['ypos'].getValue() + 50))
        node['file'].setValue(selected_node['file'].getValue())
        node['first'].setValue(int(nuke.Root()['first_frame'].getValue()))
        node['last'].setValue(int(nuke.Root()['last_frame'].getValue()))
        node['origfirst'].setValue(int(nuke.Root()['first_frame'].getValue()))
        node['origlast'].setValue(int(nuke.Root()['last_frame'].getValue()))
        node['colorspace'].setValue(int(selected_node['colorspace'].getValue()))


def script_version_up_and_create_read_from_write():
    create_read_from_write()
    nukescripts.script_and_write_nodes_version_up()
    write_version_up()



nuke.addOnUserCreate(create_write_dir, nodeClass='Write')
nuke.addBeforeRender(before_render)
nuke.addAfterRender(script_version_up_and_create_read_from_write)


