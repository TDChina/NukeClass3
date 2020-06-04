from PySide2 import QtWidgets

from model import VersionTableModel


class VersionTableView(QtWidgets.QTableView):
    def __init__(self, header_list, parent=None):
        super(VersionTableView, self).__init__(parent)
        self.header_list = header_list
        self.model = VersionTableModel()
        self.model.setHeaders(header_list)
        self.setModel(self.model)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.resizeHeader()

    def resizeHeader(self):
        if not self.header_list:
            return None
        self.resizeColumnsToContents()
