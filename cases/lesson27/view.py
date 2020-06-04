from PySide2 import QtCore, QtWidgets


class PackageToolUI(QtWidgets.QWidget):

    def __init__(self):
        super(PackageToolUI, self).__init__(None, QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Package Nuke Script')
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setFixedWidth(400)
        self.folder_layout = QtWidgets.QHBoxLayout()
        self.folder_label = QtWidgets.QLabel('Destination Folder:')
        self.folder_line = QtWidgets.QLineEdit()
        self.folder_button = QtWidgets.QPushButton('Select')
        self.folder_explorer = QtWidgets.QFileDialog()
        self.folder_layout.addWidget(self.folder_label)
        self.folder_layout.addWidget(self.folder_line)
        self.folder_layout.addWidget(self.folder_button)
        self.run_button = QtWidgets.QPushButton('Package Now!')
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.message = QtWidgets.QLabel()
        self.layout().addLayout(self.folder_layout)
        self.layout().addWidget(self.run_button)
        self.layout().addWidget(self.progress_bar)
        self.layout().addWidget(self.message)

        self.thread_pool = []
        self.close_flag = False
        self.close_timer = QtCore.QTimer()

    def closeEvent(self, event):
        if not self.thread_pool:
            self.refresh_ui()
            event.accept()
        else:
            for thread in self.thread_pool:
                thread.run_flag = False
            if not self.close_flag:
                self.close_timer.start(1000),
                event.ignore()
            else:
                event.accept()

    def refresh_ui(self):
        self.progress_bar.reset()
        self.message.clear()
        self.folder_line.clear()

    def show_message(self, msg):
        self.message.setText(msg)
