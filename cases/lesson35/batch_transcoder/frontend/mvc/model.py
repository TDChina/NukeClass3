from Qt import QtCore


def get_value(data, attr):
    value = data.get(attr, None)
    if value:
        if not isinstance(value, (str, unicode)):
            return str(value)
        else:
            return value.decode('utf-8')
    else:
        return ''


class SourceInfoModel(QtCore.QAbstractTableModel):

    update_data = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super(SourceInfoModel, self).__init__(parent)
        self.data_list = []
        self.header_list = []
        self.return_data = {}

    def columnCount(self, index=QtCore.QModelIndex()):
        return len(self.header_list)

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.data_list)

    def setHeaders(self, header_list):
        self.header_list = header_list

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if not self.header_list or section >= len(self.header_list):
            return None
        if orientation != QtCore.Qt.Horizontal:
            return None
        if role == QtCore.Qt.DisplayRole:
            return self.header_list[section]['name']
        return None

    def setDataList(self, data_list):
        self.beginResetModel()
        self.data_list = data_list
        for row in self.data_list:
            self.return_data[row['parameter']] = row['value']
        self.endResetModel()

    def currentData(self, index):
        key_name = self.header_list[index.column()]['attr']
        result = get_value(self.data_list[index.row()], key_name)
        return result

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return self.currentData(index)

    def flags(self, index):
        flags = super(SourceInfoModel, self).flags(index)
        if index.column() == 1:
            return QtCore.Qt.ItemIsEditable | flags
        return flags

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return None
        if role == QtCore.Qt.EditRole:
            key_name = self.header_list[index.column()]['attr']
            self.data_list[index.row()][key_name] = value
            self.dataChanged.emit(index, index.parent())
            self.return_data[
                self.data_list[index.row()]['parameter']] = str(value)
            self.update_data.emit(self.return_data)
            return True
        return False
