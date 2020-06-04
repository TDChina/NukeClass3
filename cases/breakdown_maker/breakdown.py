setting = '''
    input.first {input_first}
    input.first_lock true
    input.last {input_last}
    input.last_lock true
    output.first {output_first}
    output.first_lock true
    output.last {output_last}
    output.last_lock true
'''


def set_rollback(parent):
    rollback = nuke.toNode('Rollback')
    setting = '''
        input.first {input_first}
        input.first_lock true
        input.last {input_last}
        input.last_lock true
        reverse true
        output.first {output_first}
        output.first_lock true
        output.last {output_last}
        output.last_lock true
        speed 3
    '''
    input_first = parent['breakdown_frame'].value()
    input_last = parent['breakdown_frame'].value()+ 2*nuke.root()['fps'].value()
    output_first = rollback['input.last'].value()+1
    output_last = output_first + 16
    setting = setting.format(input_first=input_first,
                             input_last=input_last,
                             output_first=output_first,
                             output_last=output_last)
    rollback.readKnobs(setting)


def set_after_wipe(parent):
    node = nuke.toNode('after_wipe')

    input_first = parent['breakdown_frame'].value()
    input_last = nuke.toNode('final').lastFrame()
    output_first = nuke.toNode('final_range')['last_frame'].value()+1
    output_last = output_first - input_first + input_last

    node_setting = setting.format(input_first=input_first,
                                  input_last=input_last,
                                  output_first=output_first,
                                  output_last=output_last)
    node.readKnobs(node_setting)


def set_wipe_retime(parent):
    node = nuke.toNode('wipe_retime')

    input_first = parent['breakdown_frame'].value()-5
    input_last = nuke.toNode('final_range')['last_frame'].value()
    output_first = input_last+1
    output_last = output_first - input_first + input_last

    node_setting = setting.format(input_first=input_first,
                                  input_last=input_last,
                                  output_first=output_first,
                                  output_last=output_last)
    node.readKnobs(node_setting)


def set_after_rollback(parent):
    node = nuke.toNode('after_rollback_wipe')

    input_first = parent['breakdown_frame'].value()+1
    input_last = nuke.toNode('final').lastFrame()
    output_first = nuke.toNode('wipe_retime')['output.last'].value()+1
    output_last = output_first - input_first + input_last

    node_setting = setting.format(input_first=input_first,
                                  input_last=input_last,
                                  output_first=output_first,
                                  output_last=output_last)
    node.readKnobs(node_setting)


def set_after_card(parent):
    node = nuke.toNode('after_card')
    ref = nuke.toNode('card_range')
    node['input.first'].setValue(parent['breakdown_frame'].value()+1)
    if ref.Class() == 'Retime':
        node['output.first'].setValue(ref['output.last'].value()+1)
    elif ref.Class() == 'FrameRange':
        node['output.first'].setValue(ref['last_frame'].value()+1)
    node['input.first_lock'].setValue(True)
    node['output.first_lock'].setValue(True)


def set_explode_transform(parent):
    hold_start = parent['breakdown_first'].value()
    hold_end = parent['breakdown_last'].value()
    start = hold_start - parent['transition_frames'].value()
    end = hold_end + parent['transition_frames'].value()

def breakdown_maker_knob_changed():
    parent = nuke.thisNode()
    set_rollback(parent)
    set_after_wipe(parent)
    set_wipe_retime(parent)
    set_after_rollback(parent)
    set_after_card(parent)
    

nuke.toNode('BreakdownMaker1')['knobChanged'].setValue('breakdown_maker_knob_changed()')


def create_inputs():
    maker = nuke.thisNode()
    count = int(maker['input_addition'].value())

    for i in range(count):
        nukescripts.misc.clear_selection_recursive()
        maker.begin()
        for node in nuke.toNode('input_template').getNodes():
            node.setSelected(True)
        nuke.nodeCopy('add input')
        nukescripts.misc.clear_selection_recursive()
        nuke.nodePaste('add input')
        maker.end()