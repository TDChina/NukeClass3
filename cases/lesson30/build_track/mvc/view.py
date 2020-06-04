from PySide2 import QtWidgets

from constants import TABLE_HEADER
from version_table.view import VersionTableView


class BuildTrackDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(BuildTrackDialog, self).__init__(parent)

        self.setWindowTitle('Build Track')
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setFixedWidth(500)

        self.project_info_layout = QtWidgets.QHBoxLayout()
        self.project_label = QtWidgets.QLabel('Project:')
        self.project_text = QtWidgets.QLineEdit()
        self.project_text.setEnabled(False)
        self.project_info_layout.addWidget(self.project_label)
        self.project_info_layout.addWidget(self.project_text)

        self.track_type_layout = QtWidgets.QHBoxLayout()
        self.step_label = QtWidgets.QLabel('Step:')
        self.step_combobox = QtWidgets.QComboBox()
        self.format_label = QtWidgets.QLabel('Format:')
        self.format_combobox = QtWidgets.QComboBox()
        self.track_type_layout.addWidget(self.step_label)
        self.track_type_layout.addWidget(self.step_combobox)
        self.track_type_layout.addWidget(self.format_label)
        self.track_type_layout.addWidget(self.format_combobox)

        self.result_table = VersionTableView(TABLE_HEADER)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.find_button = QtWidgets.QPushButton('Find')
        self.build_button = QtWidgets.QPushButton('Build')
        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.button_layout.addWidget(self.find_button)
        self.button_layout.addWidget(self.build_button)
        self.button_layout.addWidget(self.cancel_button)

        self.layout().addLayout(self.project_info_layout)
        self.layout().addLayout(self.track_type_layout)
        self.layout().addWidget(self.result_table)
        self.layout().addLayout(self.button_layout)
