import os

from Qt import QtCore, QtWidgets

from main_ui import Ui_BatchTranscoder
from source_item import Ui_SourceItemWidget
from log_dialog import Ui_SourceLogDialog


class SourceItemWidget(QtWidgets.QWidget, Ui_SourceItemWidget):
    show_info = QtCore.Signal()

    def __init__(self, parent=None):
        super(SourceItemWidget, self).__init__(parent)
        self.setupUi(self)

    def mouseReleaseEvent(self, event):
        self.show_info.emit()
        event.ignore()
        

class BatchTranscoderUI(QtWidgets.QWidget, Ui_BatchTranscoder):
    dropped = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(BatchTranscoderUI, self).__init__(parent)
        self.setupUi(self)
        self.information_table = SourceInfoView(self.information_group)
        self.information_table.setGeometry(QtCore.QRect(20, 20, 501, 251))
        self.information_table.setObjectName("information_table")
        self.source_list = QtWidgets.QWidget()
        self.source_list_layout = QtWidgets.QVBoxLayout(self.source_list)
        self.source_list.setLayout(self.source_list_layout)
        self.source_list_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scrollArea.setWidget(self.source_list)
        self.scrollArea.setWidgetResizable(True)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.dropped.emit(links)
        else:
            event.ignore()


from model import SourceInfoModel

TABLE_HEADER = [
    {
        'name': 'parameter',
        'attr': 'parameter',
        'width': 180
    },
    {
        'name': 'value',
        'attr': 'value',
        'width': 300
    }
]


class SourceInfoView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super(SourceInfoView, self).__init__(parent)
        self.header_list = TABLE_HEADER
        self.model = SourceInfoModel()
        self.model.setHeaders(TABLE_HEADER)
        self.setModel(self.model)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.resizeHeader()

    def resizeHeader(self):
        if not self.header_list:
            return None
        for index, column in enumerate(self.header_list):
            self.setColumnWidth(index, column['width'])


class LogDialog(QtWidgets.QDialog, Ui_SourceLogDialog):

    def __init__(self, parent=None):
        super(LogDialog, self).__init__(parent)
        self.setupUi(self)
