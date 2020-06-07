# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'W:\develop\tdclass\batch_transcoder\frontend\mvc\source_item.ui'
#
# Created: Sun Jun  7 12:21:34 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SourceItemWidget(object):
    def setupUi(self, SourceItemWidget):
        SourceItemWidget.setObjectName("SourceItemWidget")
        SourceItemWidget.resize(500, 80)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SourceItemWidget.sizePolicy().hasHeightForWidth())
        SourceItemWidget.setSizePolicy(sizePolicy)
        SourceItemWidget.setMinimumSize(QtCore.QSize(500, 80))
        SourceItemWidget.setWindowTitle("")
        self.verticalLayoutWidget = QtGui.QWidget(SourceItemWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 471, 67))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.select_check = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.select_check.setText("")
        self.select_check.setObjectName("select_check")
        self.horizontalLayout.addWidget(self.select_check)
        self.source_name = QtGui.QLabel(self.verticalLayoutWidget)
        self.source_name.setText("")
        self.source_name.setObjectName("source_name")
        self.horizontalLayout.addWidget(self.source_name)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.source_process_status = QtGui.QLabel(self.verticalLayoutWidget)
        self.source_process_status.setText("")
        self.source_process_status.setObjectName("source_process_status")
        self.horizontalLayout.addWidget(self.source_process_status)
        self.cancel_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.log_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.log_button.setObjectName("log_button")
        self.horizontalLayout.addWidget(self.log_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.parsing_errors = QtGui.QLabel(self.verticalLayoutWidget)
        self.parsing_errors.setText("")
        self.parsing_errors.setObjectName("parsing_errors")
        self.horizontalLayout_2.addWidget(self.parsing_errors)
        self.validation_errors = QtGui.QLabel(self.verticalLayoutWidget)
        self.validation_errors.setText("")
        self.validation_errors.setObjectName("validation_errors")
        self.horizontalLayout_2.addWidget(self.validation_errors)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.source_process_message = QtGui.QLabel(self.verticalLayoutWidget)
        self.source_process_message.setText("")
        self.source_process_message.setObjectName("source_process_message")
        self.verticalLayout.addWidget(self.source_process_message)

        self.retranslateUi(SourceItemWidget)
        QtCore.QMetaObject.connectSlotsByName(SourceItemWidget)

    def retranslateUi(self, SourceItemWidget):
        self.cancel_button.setText(QtGui.QApplication.translate("SourceItemWidget", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.log_button.setText(QtGui.QApplication.translate("SourceItemWidget", "Log", None, QtGui.QApplication.UnicodeUTF8))

