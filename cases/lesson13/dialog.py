# coding=utf-8

import re

from PySide2 import QtWidgets


class BaseDialog(QtWidgets.QDialog):

    def __init__(self):
        self.name = ''
        self.rule_pattern = None

        super(BaseDialog, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.name_label = QtWidgets.QLabel('Name:')
        self.name_edit = QtWidgets.QLineEdit()
        self.name_layout = QtWidgets.QHBoxLayout()
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_edit)
        self.layout().addLayout(self.name_layout)
        self.rule = QtWidgets.QLabel()
        self.layout().addWidget(self.rule)
        self.ok_button = QtWidgets.QPushButton('OK')
        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.additional_layout = QtWidgets.QVBoxLayout()
        self.layout().addLayout(self.additional_layout)
        self.layout().addLayout(self.button_layout)

        self.ok_button.setEnabled(False)

        self.name_edit.textEdited.connect(self._check_rule)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def _check_rule(self):
        try:
            name = str(self.name_edit.text())
            if re.match(self.rule_pattern, name):
                self.rule.setVisible(False)
                self.ok_button.setEnabled(True)
                return
        except UnicodeError:
            pass
        self.rule.setVisible(True)
        self.ok_button.setEnabled(False)

    def accept(self):
        self.name = str(self.name_edit.text())
        super(BaseDialog, self).accept()
        return True


class AddGizmoDialog(BaseDialog):
    
    def __init__(self):
        super(AddGizmoDialog, self).__init__()
        self.setWindowTitle('Add Gizmo')
        self.rule_pattern = re.compile('^[A-Za-z]{3,24}$')
        self.rule.setText('Name rule:\n'
                          '1. Use English characters only.\n'
                          '2. Length in 3 to 24 characters.\n'
                          '3. Not include space or undescore.')
        

class AddTemplateDialog(BaseDialog):

    def __init__(self):
        super(AddTemplateDialog, self).__init__()
        self.setWindowTitle('Add Nuke Template')
        self.rule_pattern = re.compile('^([A-Za-z0-9]+(\s|_)?){1,8}$')
        self.rule.setText('Name rule:\n'
                          '1. Use english words and numbers only.\n'
                          '2. No longer than 8 words.\n'
                          '2. Use space or underscore as delimiter.')


class AddPythonDialog(BaseDialog):

    def __init__(self):
        self.script = ''
        
        super(AddPythonDialog, self).__init__()

        script = QtWidgets.QApplication.instance().clipboard().text()

        self.script_editor = QtWidgets.QTextEdit()
        self.script_editor.setPlainText(script)
        self.additional_layout.addWidget(self.script_editor)

        self.setWindowTitle('Add Python Script')
        self.rule_pattern = re.compile('^([A-Za-z0-9]+_?){1,4}$')
        self.rule.setText('Name rule:\n'
                          '1. Use english words and numbers only.\n'
                          '2. No longer than 4 words.\n'
                          '2. Use underscore as delimiter.')
        
    def accept(self):
        self.script = self.script_editor.toPlainText()
        super(AddPythonDialog, self).accept()


class AddMenuDialog(BaseDialog):
    def __init__(self):
        super(AddMenuDialog, self).__init__()
        self.setWindowTitle('Add Sub Menu')
        self.rule_pattern = re.compile('^[A-Za-z]{1,12}$')
        self.rule.setText('Name rule:\n'
                          '1. Use English characters only.\n'
                          '2. No longer than 12 characters.\n'
                          '3. Not include space.')


class RemoveItemDialog(QtWidgets.QDialog):

    def __init__(self, item_names):
        super(RemoveItemDialog, self).__init__()
        self.setWindowTitle('Remove Items')
        self.setLayout(QtWidgets.QVBoxLayout())
        self.name_list = QtWidgets.QListWidget()
        self.name_list.addItems(item_names)
        self.name_list.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)

        self.ok_button = QtWidgets.QPushButton('OK')
        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout().addWidget(self.name_list)
        self.layout().addLayout(self.button_layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.delete_names = []

    def accept(self):
        for item in self.name_list.selectedItems():
            self.delete_names.append(str(item.text()))
        super(RemoveItemDialog, self).accept()
        return True
