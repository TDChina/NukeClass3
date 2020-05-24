# _*_ coding: utf-8 _*_
# @Time      : 5/21/2020 11:40 PM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : dailies_render.py
# @software  : PyCharm

import os

import nuke
import nukescripts
import thread

class DailiesRenderPanel(nukescripts.panels.PythonPanel):

    def __init__(self):
        super(DailiesRenderPanel,self).__init__('Dailies Render')
        self.initUI()

    def initUI(self):
        self.file_knob = nuke.File_Knob('source','image sequence')
        self.source_list = nuke.Multiline_Eval_String_Knob('source_list','sources')
        self.source_list.setEnabled(False)
        self.remove_first = nuke.Int_Knob('remove_first', 'remove first line')
        self.remove_last = nuke.Int_Knob('remove_last', 'remove last line')
        self.remove_first.setValue(1)
        self.remove_last.setValue(1)
        self.remove_last.clearFlag(nuke.STARTLINE)
        self.remove_button = nuke.PyScript_Knob('remove', 'remove')
        self.create_button = nuke.PyScript_Knob('create', 'create node tree')
        self.render_button = nuke.PyScript_Knob('render', 'render dailies')
        self.create_button.setFlag(nuke.STARTLINE)
        self.message = nuke.Text_Knob('message', '',' ')
        self.addKnob(self.file_Knob)
        self.addKnob(self.source_list)
        self.addKnob(self.remove_first)
        self.addKnob(self.remove_last)
        self.addKnob(self.remove_button)
        self.addKnob(self.create_button)
        self.addKnob(self.render_button)
        self.addKnob(self.messsage)
        self.sources = {}
        self.bypass_callback = False

    def knobChanged(self,knob):
        if self.bypass_callback:
            return False
        try:
            func = getattr(self, 'slot_{}_knob'.format(knob.name()))
            func()
        except AttributeError:
            pass

    def slot_source_knob(self):
        self.message.setValue('')
        source = self.file_knob.value()
        for value in self.sources.values():
            if source == value.split(' ')[0]:
                self.message.setValue('source already been added')
                return False

        source_name = os.path.basename(source).split('.')[0]
        for f in nuke.getFileNameList(os.path.dirname(source)):
            if source_name in f:
                source_path = '{} {}'.format(source,f.split(' ')[1])
                break
        self.sources[source_name] = source_path
        self.source_list.setValue(self.source_list.value() + '#{} {}\n'.format())
    def slot_remove_konb(self):
        first_line = self.remove_first.value()
        last_line = self.remove_last.value()
        if last_line>self.count or last_line< first_line or first_line()<1:
            self.message.setValue('wrong line number {} to {}'.format(first_line,last_line))
            return False

        self.message.setValue('')
        sources = self.source_list.value().split('\n')
        remove_sources = sources[first_line -1:last_line]
        for source in remove_sources:
            self.sources.pop(source.split(' ')[1])
        sources = [i for i in sources if i and i not in remvoe_sources]
        sources = ['# {} {}'.format(sources.index(i)+1,i.split(' ')[1]) for i in sources]
        self.source_list.setValue('{}\n'.format('\n'.join(sources)))

    def slot_create_knob(self):
        last_read = None
        with nuke.root():
            for source_name in self.sources:
                read = nuke.createNode('Read', inpanel = False)
                read['file'].fromUserText(self.sources[source_name])
                if last_read:
                    read.setXYpos(last_read.xpos()+150,last_read.ypos())

                slate = nuke.ceateNode('Slate',inpanel = False)
                slate.setInput(0,read)
                slate.setXYpos(read.xpos(),read.ypos()+100)
                write = nuke.createNode('Write',inpanel=False)
                write.setInput(0,slate)
                write.setXYpos(slate.xpos(),slate.ypos()+100)
                self.render_infos[write.name()] = (read['first'].value(),read['last'].value())
                last_read = read
                for func in self.control_funcs.values():
                    func(self,read,slate,write)
        self.clear()

    def clear(self):
        self.bypass_callback = True
        self.sources = {}
        self.render_infos = {}
        self.file_knob.setValue('')
        self.source_list.setValue('')
        self.message.setValue('')
        self.bypass_callback = False
    def register_control(self,func):
        self.control_funcs[func.func_name] = func

    def slot_render_knob(self):
        for write in self.render_infos:
            first,last = self.render_infos[write]
            thread.start_new_thread(nuke.executeInMainThread,(nuke.execute,(write,first,last,1)))