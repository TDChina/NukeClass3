import nuke


class MultiNodeEditor(object):

    def __init__(self):
        self.editor = nuke.thisNode()
        self.all_nodes = []

    def get_nodes(self):
        node_class = self.editor['class'].value()
        node_name = self.editor['node_name'].value()
        if not node_class:
            nuke.message('You should input a node class name.')
            return
        all_nodes = [node for node in nuke.allNodes() if
                     node.Class() == node_class and
                     node_name in node.name()]
        if not all_nodes:
            nuke.message('No valid nodes could be found.')
            return
        all_nodes.sort(key=lambda x: x.name())
        self.all_nodes = all_nodes

    def get_knobs(self, mode):
        knobs = []
        knob_names = self.editor['knob_name'].value().split(',')

        if mode == 'sync':
            for name in knob_names:
                if name in self.all_nodes[0].knobs().keys():
                    knobs.append(self.all_nodes[0].knob(name))
                else:
                    nuke.message('Can not find {} in {}.'.format(name,
                                                                 self.all_nodes[
                                                                     0].name()))
                    return []

        elif mode == 'non sync':
            for node in self.all_nodes:
                node_knobs = []
                for name in knob_names:
                    if name in node.knobs().keys():
                        node_knobs.append(node.knob(name))
                    else:
                        nuke.message(
                            'Can not find {} in {}.'.format(name, node.name()))
                        return []
                knobs.append(node_knobs)
        return knobs

    def add_knobs(self, mode):
        self.remove_knobs()
        custom_knob_names = []
        if mode == 'sync':
            for node in self.all_nodes:
                name_knob = nuke.Boolean_Knob(node.name())
                name_knob.setValue(1)
                if not custom_knob_names:
                    name_knob.setFlag(nuke.STARTLINE)
                self.editor.addKnob(name_knob)
                custom_knob_names.append(name_knob.name())
            name_knob.setFlag(nuke.ENDLINE)

            for knob in self.knobs:
                self.editor.addKnob(knob)
                custom_knob_names.append(knob.name())

            update_knob = nuke.PyScript_Knob('update', 'set all values')
            update_knob.setFlag(nuke.STARTLINE)
            update_knob.setCommand('MultiNodeEditor.set_all_values()')
            self.editor.addKnob(update_knob)
            custom_knob_names.append(update_knob.name())

        elif mode == 'non sync':
            for i in range(len(self.all_nodes)):
                name_knob = nuke.Boolean_Knob(self.all_nodes[i].name())
                name_knob.setValue(1)
                name_knob.setFlag(nuke.STARTLINE)
                self.editor.addKnob(name_knob)
                custom_knob_names.append(name_knob.name())
                for knob in self.knobs[i]:
                    self.editor.addKnob(knob)
                    custom_knob_names.append(knob.name())
        self.editor['custom_knobs'].setValues(custom_knob_names)

    @staticmethod
    def set_all_values():
        editor = nuke.thisNode()
        nodes = []
        knobs = []
        for i in range(editor['custom_knobs'].numValues()):
            name = editor['custom_knobs'].enumName(i)
            if not name or name == 'update':
                continue
            knob = editor[name]
            if isinstance(knob, nuke.Boolean_Knob):
                if knob.value():
                    with nuke.Root():
                        nodes.append(nuke.toNode(name))
                else:
                    continue
            else:
                knobs.append(knob)

        for node in nodes:
            for knob in knobs:
                node[knob.name()].setValue(knob.value())

    @staticmethod
    def remove_knobs():
        editor = nuke.thisNode()
        for i in range(editor['custom_knobs'].numValues()):
            name = editor['custom_knobs'].enumName(i)
            if name:
                editor.removeKnob(editor.knob(name))
        editor['custom_knobs'].setValues([])

    def run(self):
        self.get_nodes()
        if self.all_nodes:
            mode = self.editor['mode'].value()
            self.knobs = self.get_knobs(mode)

            if not self.knobs:
                return
            self.add_knobs(mode)
