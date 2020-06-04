import os
import nuke

READ_CLASSES = [
    'Read',
    'DeepRead',
    'ReadGeo2',
    'ReadGeo',
    'Camera2',
    'Vectorfield'
]


def get_all_nodes(node_class=None):
    if node_class:
        return nuke.allNodes(node_class, recurseGroups=True)
    else:
        return nuke.allNodes(recurseGroups=True)


def get_read_nodes():
    nodes = []
    for node_class in READ_CLASSES:
        nodes.extend(get_all_nodes(node_class))
    return nodes


def modify_path(node):
    if node.Class() == 'Vectorfield':
        knob_name = 'vfield_file'
    else:
        knob_name = 'file'
    source = node[knob_name].value()
    basename = os.path.basename(source)

    if os.path.isfile(source):
        node[knob_name].setValue(
            '[file dirname [value root.name]]/sources/' + basename)
    else:
        node['file'].setValue(('[file dirname [value root.name]]/sources/'
                               '{}/{}').format(basename.split('.')[0],
                                               basename))


def frame_to_pattern(frame_path):
    name_list = frame_path.split('.')
    name_list[-2] = '%04d'
    return '.'.join(name_list).replace('\\', '/')
