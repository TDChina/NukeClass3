import os
import nuke


def show_read_file_name(node):
    fname = os.path.basename(node.input(0)['file'].value())
    node['watermark_name'].setValue(fname)
    return fname


def add_checkbox_by_name(node, name):
    index = 0
    for name_part in name.split('_'):
        if '.' not in name_part:
            k = nuke.Boolean_Knob('u_{}_{}'.format(index, name_part), name_part)
            k.setValue(1)
            node.addKnob(k)
            index += 1
        else:
            first = True
            for part in name_part.split('.'):  #td_010_0010_comp_v002.%04d.jpg
                if first:
                    k = nuke.Boolean_Knob('u_{}_{}'.format(index, part), part)
                    first = False
                else:
                    k = nuke.Boolean_Knob('d_{}_{}'.format(index, part), part)
                k.setValue(1)
                node.addKnob(k)
                index += 1




def change_name(node):
    name = ''
    part_knobs = [k for k in node.allKnobs() if k.name().startswith('u_') or k.name().startswith('d_')]
    count = len(part_knobs)
    part_knobs = [k for k in part_knobs if k.value()]
    for i in range(count):
        for k in part_knobs:
            if k.name().startswith('u_{}'.format(i)):
                name += '_{}'.format(k.label())
            elif k.name().startswith('d_{}'.format(i)):
                name += '.{}'.format(k.label())
    name = name[1:]
    node['watermark_name'].setValue(name)


def on_knob_changed():
    n = nuke.thisNode()
    k = nuke.thisKnob()
    if k.name() == 'inputChange':
        if n.inputs() and n.input(0).Class() == 'Read':
            fname = show_read_file_name(n)
            add_checkbox_by_name(n, fname)
        else:
            clear_name(n)