# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'W:\develop\tdclass\batch_transcoder\frontend\mvc\log_dialog.ui'
#
# Created: Sun Jun  7 15:27:05 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SourceLogDialog(object):
    def setupUi(self, SourceLogDialog):
        SourceLogDialog.setObjectName("SourceLogDialog")
        SourceLogDialog.resize(400, 314)
        self.button_box = QtGui.QDialogButtonBox(SourceLogDialog)
        self.button_box.setGeometry(QtCore.QRect(120, 280, 151, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.log_text_browser = QtGui.QTextBrowser(SourceLogDialog)
        self.log_text_browser.setGeometry(QtCore.QRect(10, 10, 381, 261))
        self.log_text_browser.setObjectName("log_text_browser")

        self.retranslateUi(SourceLogDialog)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL("accepted()"), SourceLogDialog.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL("rejected()"), SourceLogDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SourceLogDialog)

    def retranslateUi(self, SourceLogDialog):
        SourceLogDialog.setWindowTitle(QtGui.QApplication.translate("SourceLogDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

