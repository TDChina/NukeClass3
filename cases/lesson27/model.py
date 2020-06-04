import os
import nuke

from utils import get_read_nodes, modify_path

class NukePackageWrapper(object):
    def __init__(self, dest_root):
        self.error_nodes = []
        self.single_results = []
        self.sequence_results = {}
        self.copy_files_count = 0
        self.dest_root = dest_root
        self.original_nk = nuke.Root().name()
        self.nodes = [node for node in get_read_nodes() if self.check_node_error(node)]

    def check_node_error(self, node):
        if node.hasError():
            self.error_nodes.append(node.name())
            return False
        return True

    def get_node_source(self, node):
        knob_name = 'file'
        if node.Class() == 'Vectorfield':
            knob_name = 'vfield_file'
        source = node[knob_name].value()
        if os.path.isfile(source):
            self.single_results.append((node.name(), source))
            self.copy_files_count += 1
        elif '%04d' in source:
            self.get_sequence_source(node, source, '%04d')
        elif '####' in source:
            self.get_sequence_source(node, source, '####')
        else:
            return

    def get_sequence_source(self, node, source, pattern):
        source_files = []
        first = node['first'].value()
        last = node['last'].value()
        for frame in range(first, last + 1):
            source_file = source.replace(pattern, str(frame).zfill(4))
            if os.path.isfile(source_file):
                source_files.append(source_file)
                self.copy_files_count += 1
        if source_files:
            basename = '.'.join(os.path.basename(source).split('.')[:-2])
            self.sequence_results[basename] = (node.name(),
                                               source_files,
                                               first,
                                               last)
        else:
            self.error_nodes.append(node.name())

    def grab_source(self, index):
        self.get_node_source(self.nodes[index])

    def modify_nodes_path(self):
        nuke.scriptSaveAs('{}/{}'.format(self.dest_root,
                                         os.path.basename(nuke.Root().name())),
                          1)
        for node in self.nodes:
            modify_path(node)
        nuke.scriptSave()
        nuke.scriptClear()
        nuke.scriptOpen(self.original_nk)













