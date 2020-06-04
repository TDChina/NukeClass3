import os

import hiero.ui
from hiero.exporters.FnTranscodeExporterUI import TranscodeExporterUI

from PySide2 import QtCore, QtWidgets

from watermark_exporter import WatermarkTranscode, WatermarkTranscodePreset


default_config = {
    'add_image': True,
    'watermark_image_path': 'W:/develop/tdclass/lesson31/watermark_1080p.png',
    'read_premult': True,
    'transform_x': '0',
    'transform_y': '0'
}


class WatermarkTranscodeUI(TranscodeExporterUI):
    def __init__(self, preset):
        """Initialize"""
        super(WatermarkTranscodeUI, self).__init__(preset)

        self._displayName = "Watermark Transcode"
        self._taskType = WatermarkTranscode

    def get_watermark_path(self):
        image_path = QtWidgets.QFileDialog().getOpenFileName(filter='*.png')
        if os.path.isfile(image_path[0]):
            self.image_path_edit.setText(image_path[0])

    def set_add_image(self, state):
        self._preset._properties["add_image"] = state == QtCore.Qt.Checked

    def set_image_path(self):
        self._preset._properties["watermark_path"] = self.image_path_edit.text()

    def set_premult(self, state):
        self._preset._properties["watermark_premult"] = state == QtCore.Qt.Checked

    def set_transform(self):
        self._preset._properties["watermark_transform"] = '{%s %s}' % (self.transform_x.text(), self.transform_y.text())

    def check_preset(self):
        if "add_image" not in self._preset._properties:
            self._preset._properties["add_image"] = True if default_config["add_image"] else False
        if "watermark_path" not in self._preset._properties:
            self._preset._properties["watermark_path"] = default_config["watermark_image_path"]
        if "watermark_premult" not in self._preset._properties:
            self._preset._properties["watermark_premult"] = True if default_config["read_premult"] else False
        if "watermark_transform" not in self._preset._properties:
            self._preset._properties["watermark_transform"] = '{%s %s}' % (
            default_config["transform_x"], default_config["transform_y"])

    def populateUI(self, widget, exportTemplate):
        watermark_setting = QtWidgets.QVBoxLayout()
        watermark_image_setting = QtWidgets.QHBoxLayout()
        watermark_properties_setting = QtWidgets.QHBoxLayout()

        watermark_setting.addLayout(watermark_image_setting)
        watermark_setting.addLayout(watermark_properties_setting)

        self.check_preset()

        self.image_check = QtWidgets.QCheckBox('Add Image')
        self.image_check.setCheckState(QtCore.Qt.Checked if self._preset._properties["add_image"] else Qt.Unchecked)
        image_label = QtWidgets.QLabel('Image Path:')
        self.image_path_edit = QtWidgets.QLineEdit()
        self.image_path_edit.setText(self._preset._properties['watermark_path'])
        self.image_file_button = QtWidgets.QPushButton('Find')
        watermark_image_setting.addWidget(self.image_check)
        watermark_image_setting.addWidget(image_label)
        watermark_image_setting.addWidget(self.image_path_edit)
        watermark_image_setting.addWidget(self.image_file_button)
        self.premult = QtWidgets.QCheckBox('Read Node Premult')
        self.premult.setCheckState(QtCore.Qt.Checked if self._preset._properties["watermark_premult"] else Qt.Unchecked)
        transform_label = QtWidgets.QLabel('Watermark Transform:')
        self.transform_x = QtWidgets.QLineEdit()
        self.transform_y = QtWidgets.QLineEdit()
        self.transform_x.setText(self._preset._properties["watermark_transform"].split(' ')[0].replace('{',''))
        self.transform_y.setText(self._preset._properties["watermark_transform"].split(' ')[1].replace('}', ''))
        watermark_properties_setting.addWidget(self.premult)
        watermark_image_setting.addSpacing(50)
        watermark_properties_setting.addWidget(transform_label)
        watermark_properties_setting.addWidget(self.transform_x)
        watermark_properties_setting.addWidget(self.transform_y)

        self.image_check.stateChanged.connect(self.set_add_image)
        self.image_file_button.clicked.connect(self.get_watermark_path)
        self.image_path_edit.textChanged.connect(self.set_image_path)
        self.premult.stateChanged.connect(self.set_premult)
        self.transform_x.textChanged.connect(self.set_transform)
        self.transform_y.textChanged.connect(self.set_transform)

        widget.layout().addLayout(watermark_setting)

        super(WatermarkTranscodeUI, self).populateUI(widget, exportTemplate)


hiero.ui.taskUIRegistry.registerTaskUI(WatermarkTranscodePreset, WatermarkTranscodeUI)
