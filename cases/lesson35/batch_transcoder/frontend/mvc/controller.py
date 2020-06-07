import copy
import json
import re
import shutil
import time

import yaml
from Qt import QtCore

from batch_transcoder.frontend.mvc.view import LogDialog

from batch_transcoder.backend.source.service import SourceService
from batch_transcoder.backend.config.service import ConfigService
from batch_transcoder.backend.validation.service import ValidationService
from batch_transcoder.backend.parsing.service import ParsingService
from batch_transcoder.backend.template.service import TemplateService

from batch_transcoder.frontend.mvc.view import SourceItemWidget

from batch_transcoder.backend.utils.thread import ExecuteThread

from batch_transcoder.backend.utils.constants import TEMP_PATH
from batch_transcoder.gateway.nuke_transcode import run_nuke_transcode

class SourceItemController(object):

    def __init__(self, source, widget):
        self.source = source
        self.widget = widget
        self._connect_slots()
        self._callbacks = {}
        self.validators = []
        self.parsers = []
        self._validation_logs = []
        self._parsing_logs = []

    def register_callback(self, event, func):
        self._callbacks[event] = func

    def _connect_slots(self):
        self.widget.show_info.connect(self.emit_data)
        self.widget.log_button.clicked.connect(self.show_log)

    @property
    def log_text(self):
        logs = []
        logs.extend(self._parsing_logs)
        logs.extend(self._validation_logs)
        return '\n\n'.join(logs)

    def show_log(self):
        dialog = LogDialog(self.widget)
        dialog.log_text_browser.setPlainText(self.log_text)
        dialog.exec_()

    def emit_data(self):
        func = self._callbacks['show_info']
        func(self)

    @property
    def status(self):
        return self.widget.source_process_status.text()

    @status.setter
    def status(self, value):
        self.widget.source_process_status.setText(value)

    def set_validators(self, validators):
        self.validators = validators

    def set_parsers(self, parsers):
        self.parsers = parsers

    def set_validate_result(self, errors):
        message = ','.join([e.__class__.__name__ for e in errors])
        self.widget.validation_errors.setText(message)
        self._validation_logs = []
        for error in errors:
            self._validation_logs.append(
                '{}: {}'.format(error.__class__.__name__, str(error))
            )
        if not any([str(self.widget.validation_errors.text()),
                    str(self.widget.parsing_errors.text())]):
            self.widget.source_process_status.setText('Ready')
            self.widget.select_check.setCheckState(QtCore.Qt.Checked)
        else:
            self.widget.source_process_status.setText('Error')
            self.widget.select_check.setCheckState(QtCore.Qt.Unchecked)

    def set_parsing_data(self, result):
        self.source.data = result

    def set_parsing_errors(self, errors):
        message = ','.join([e.__class__.__name__ for e in errors])
        self.widget.parsing_errors.setText(message)
        self._parsing_logs = []
        for error in errors:
            self._parsing_logs.append(
                '{}: {}'.format(error.__class__.__name__, str(error))
            )
        if not any([str(self.widget.validation_errors.text()),
                    str(self.widget.parsing_errors.text())]):
            self.widget.source_process_status.setText('Ready')
            self.widget.select_check.setCheckState(QtCore.Qt.Checked)
        else:
            self.widget.source_process_status.setText('Error')
            self.widget.select_check.setCheckState(QtCore.Qt.UnChecked)


class SourceItemFactory(object):

    def __init__(self, config_service):
        self.source_service = SourceService(config_service)
        self._validation_service = ValidationService(config_service)
        self.parsing_service = ParsingService(config_service)
        self._drag_in_validators = []

    def _run_drag_in_validators(self, path):
        exceptions = []
        for validator in self._drag_in_validators:
            exceptions.extend(validator.validate(path))
        return exceptions

    def create_source(self, path):
        sources = self.source_service.add_source(path)
        source_controllers = []
        for source in sources:
            exceptions = self._run_drag_in_validators(source)
            if exceptions:
                continue
            widget = SourceItemWidget()
            widget.source_name.setText(source.name)
            controller = SourceItemController(source, widget)
            controller.set_parsers(self.parsing_service.get_parsers())
            controller.set_validators(
                self._validation_service.get_source_validators())
            source_controllers.append(controller)
        return source_controllers


class TranscodingController(object):

    def __init__(self, config_service):
        self._config_service = config_service
        self._template_service = TemplateService(config_service)
        self._source_controllers = []

    def set_sources(self, source_controllers):
        self._source_controllers = source_controllers

    def run(self):
        template = self._template_service.get_template_file()
        for controller in self._source_controllers:
            if not controller.status in ('', 'Ready'):
                continue
            data = controller.source.data
            if controller.source.sequence.length() == 1:
                data['source_path'] = '{}/{}'.format(
                    controller.source.root,
                    controller.source.sequence.head())
            else:
                data['source_path'] = '{}/{}####{}'.format(
                    controller.source.root,
                    controller.source.sequence.head(),
                    controller.source.sequence.tail())
            data['dest_path'] = self._config_service.get_preset_config(
                'transcoding/dest_pattern').format(**data)
            for key in data:
                if isinstance(data[key], str) and re.match(r'\d+', data[key]):
                    data[key] = int(data[key])
            template_path = self._save_temp_template_data(template, data)
            controller.status = 'Rendering'
            controller.widget.setEnabled(False)
            try:
                run_nuke_transcode(template_path)
                controller.status = 'Done'
            except:
                controller.status = ''
            controller.widget.setEnabled(True)

    @staticmethod
    def _save_temp_template_data(template, data):
        timestramp = time.strftime('%Y%m%d%H%M%S')
        shutil.copy2(template, '{}/template_{}.nk'.format(TEMP_PATH, timestramp))
        with open('{}/parameter_{}.json'.format(TEMP_PATH, timestramp), 'w') as f:
            json.dump(data, f, indent=4)
        return '{}/template_{}.nk'.format(TEMP_PATH, timestramp)


class BatchTranscoderController(object):

    def __init__(self, view):
        self._view = view
        self.config_service = ConfigService()
        self._source_factory = SourceItemFactory(self.config_service)
        self._transcoding_controller = TranscodingController(self.config_service)
        self._template_service = TemplateService(self.config_service)
        self.source_controllers = []
        self.current_source_controller = None
        self.validation_thread = None
        self._connect_slots()
        self.init_ui()

    def init_ui(self):
        self._view.show_list.clear()
        self._view.show_list.addItems(self.config_service.get_show_list())

    def _connect_slots(self):
        self._view.dropped.connect(self.add_source)
        self._view.show_list.currentIndexChanged.connect(
            self.update_preset_list)
        self._view.preset_list.currentIndexChanged.connect(self.update_config)
        self._view.information_table.model.update_data.connect(
            self.update_source_info)
        self._view.run_button.clicked.connect(self.run_transcoding)

    def update_source_info(self, data):
        self.current_source_controller.set_parsing_data(copy.deepcopy(data))
        self._run_validators(self.current_source_controller)

    @property
    def show(self):
        return self._view.show_list.currentText()

    @property
    def preset(self):
        return self._view.preset_list.currentText()

    def update_config(self):
        self.clear_source_list()
        self.clear_information_table()
        if self.show and self.preset:
            self.config_service.update_context(self.show, self.preset)

    def update_preset_list(self):
        self._view.preset_list.clear()
        self._view.preset_list.addItems(
            self.config_service.get_preset_list(self.show))

    def clear_information_table(self):
        self._view.information_table.model.setDataList([])

    def clear_source_list(self):
        for i in range(len(self.source_controllers)):
            item = self._view.source_list_layout.takeAt(0)
            item.widget().deleteLater()
        for con in self.source_controllers:
            del con
        self.source_controllers = []

    @staticmethod
    def _run_validators(con):
        result = []
        for validator in con.validators:
            result.extend(validator.validate(con.source))
        con.set_validate_result(result)

    def _run_parsers(self, con):
        exceptions = []
        current_data = {}
        for parser in con.parsers:
            try:
                current_data = parser.parse(con.source, current_data)
            except Exception as e:
                exceptions.append(e)
                continue
        con.set_parsing_data(current_data)
        self._assemble_template_parameter_keys(con)
        if exceptions:
            con.set_parsing_errors(exceptions)

    def add_source(self, path_list):
        for path in path_list:
            source_controllers = self._source_factory.create_source(path)
            if not source_controllers:
                continue
            for controller in source_controllers:
                controller.register_callback('show_info', self.show_source_info)
                self.source_controllers.append(controller)
                self._view.source_list_layout.addWidget(controller.widget)

                parsing_thread = ExecuteThread(self._run_parsers,
                                               (controller,),
                                               parent=self._view)
                validation_thread = ExecuteThread(self._run_validators,
                                                  (controller,),
                                                  parent=self._view)
                parsing_thread.finished.connect(validation_thread.start)
                parsing_thread.start()
                
    def _assemble_template_parameter_keys(self, controller):
        parameter_file = self._template_service.get_parameter_file()
        if not parameter_file:
            return
        with open(parameter_file) as f:
            parameters = yaml.safe_load(f)
        for key in parameters.get('parameters'):
            if key not in controller.source.data:
                controller.source.data[key] = str(parameters.get('parameters')[key] or '')

    def show_source_info(self, controller):
        self.current_source_controller = controller
        data = controller.source.data
        table_data = []
        keys = sorted(data.keys())
        for key in keys:
            table_data.append({'parameter': key, 'value': data[key]})
        self._view.information_table.model.setDataList(table_data)

    def run_transcoding(self):
        self._transcoding_controller.set_sources(self.source_controllers)
        transcode_thread = ExecuteThread(self._transcoding_controller.run, parent=self._view)
        transcode_thread.start()
