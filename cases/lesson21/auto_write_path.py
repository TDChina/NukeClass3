import os
import re

import nuke
import nukescripts


class AutoWritePath(nukescripts.PythonPanel):

    def __init__(self, root_path):
        super(AutoWritePath, self).__init__()
        self.root_path = root_path

        self.setMinimumSize(550, 160)
        self.show_knob = nuke.String_Knob('show', 'Show:')
        self.episode_knob = nuke.String_Knob('episode', 'Episode:')
        self.episode_knob.clearFlag(nuke.STARTLINE)
        self.sequence_knob = nuke.String_Knob('seq', 'Sequence:')
        self.sequence_knob.clearFlag(nuke.STARTLINE)
        self.shot_knob = nuke.String_Knob('shot', 'Shot:')
        self.shot_knob.clearFlag(nuke.STARTLINE)
        self.step_knob = nuke.String_Knob('step', 'Step:')
        self.task_knob = nuke.Enumeration_Knob('task', 'Task:', [])
        self.task_knob.clearFlag(nuke.STARTLINE)
        self.version_knob = nuke.Enumeration_Knob('version', 'Version', [])
        self.version_knob.clearFlag(nuke.STARTLINE)
        self.format_knob = nuke.Enumeration_Knob('format', 'File Type:',
                                                 ['exr', 'dpx', 'jpg', 'tiff', 'mov'])
        self.format_knob.clearFlag(nuke.STARTLINE)
        self.name_knob = nuke.String_Knob('name', 'File Name:')
        self.path_knob = nuke.File_Knob('path', 'Write Path:')

        self.addKnob(self.show_knob)
        self.addKnob(self.episode_knob)
        self.addKnob(self.sequence_knob)
        self.addKnob(self.shot_knob)
        self.addKnob(self.step_knob)
        self.addKnob(self.task_knob)
        self.addKnob(self.version_knob)
        self.addKnob(self.format_knob)
        self.addKnob(self.name_knob)
        self.addKnob(self.path_knob)

        self.episode_knob.setVisible(False)

        self.path_pattern = None
        self.write_path_pattern = None
        self.task_names = {}

    def set_path_pattern(self, pattern):
        self.path_pattern = pattern

    def set_task_names(self, name_dict):
        self.task_names = name_dict

    def set_write_path_pattern(self, pattern):
        self.write_path_pattern = pattern

    def use_episode(self, use_episode):
        self.episode_knob.setVisible(use_episode)

    def parse_parameters(self):
        match = re.match(self.path_pattern, self.root_path)
        if match:
            path_info = match.groupdict()
            self.show_knob.setValue(path_info.get('show'))
            self.episode_knob.setValue(path_info.get('episode'))
            self.sequence_knob.setValue(path_info.get('sequence'))
            self.shot_knob.setValue(path_info.get('shot'))
            self.step_knob.setValue(path_info.get('step'))
            self.version_knob.setValues([path_info.get('version'),
                                         'v' + str(int(path_info.get('version')[1:])+1).zfill(3)])
            return True
        else:
            nuke.message('Can not parse valid values from root path.')
            self.cancel()
            return False

    def fill_step_tasks(self):
        step = self.step_knob.value()
        if step in self.task_names:
            self.task_knob.setValues(self.task_names[step])

    def knobChanged(self, knob):
        if not self.write_path_pattern:
            return
        parameters = {
            'show': self.show_knob.value(),
            'episode': self.episode_knob.value(),
            'sequence': self.sequence_knob.value(),
            'shot': self.shot_knob.value(),
            'step': self.step_knob.value(),
            'task': self.task_knob.value(),
            'version': self.version_knob.value(),
            'format': self.format_knob.value()
        }
        if parameters['format'] != 'mov':
            parameters['format'] = '%04d.{}'.format(parameters['format'])
        if knob.name() == 'name':
            self.path_knob.setValue('{}/{}'.format(os.path.dirname(self.path_knob.value()),
                                                   self.name_knob.value()))
        elif knob.name() == 'path':
            self.name_knob.setValue(os.path.basename(self.path_knob.value()))
        else:
            path = self.write_path_pattern.format(**parameters)
            self.name_knob.setValue(os.path.basename(path))
            self.path_knob.setValue(path)

    def show(self):
        if not self.parse_parameters():
            return
        self.fill_step_tasks()
        result = nukescripts.PythonPanel.showModalDialog(self)
        if result:
            write = nuke.createNode('Write')
            write['file'].fromUserText(self.path_knob.value())


def auto_write_path(path_pattern=None, task_names={}, write_path_pattern=None):
    script_path = nuke.root().name()
    if not script_path.endswith('.nk'):
        nuke.message('Nuke script unsaved.')
        return
    panel = AutoWritePath(script_path)
    panel.set_path_pattern(path_pattern)
    panel.set_task_names(task_names)
    panel.set_write_path_pattern(write_path_pattern)
    panel.show()
