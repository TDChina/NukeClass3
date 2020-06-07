from Qt import QtCore


class ExecuteThread(QtCore.QThread):

    finished = QtCore.Signal()

    def __init__(self, func, args=(), kwargs={}, parent=None):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        super(ExecuteThread, self).__init__(parent)

    def run(self):
        self.func(*self.args, **self.kwargs)
        self.finished.emit()
