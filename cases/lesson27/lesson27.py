import time
from PySide2 import QtCore, QtWidgets

class Worker(QtCore.QThread):
	finish = QtCore.Signal()

	def __init__(self):
		super(Worker, self).__init__()

	def run(self):
		time.sleep(3)
		self.finish.emit()

class UI(QtWidgets.QWidget):
	def __init__(self):
		super(UI, self).__init__()
		self.setLayout(QtWidgets.QVBoxLayout())
		self.button = QtWidgets.QPushButton('run')
		self.message = QtWidgets.QLabel()
		self.layout().addWidget(self.button)
		self.layout().addWidget(self.message)
		self.worker = Worker()
		self.worker.finish.connect(self.update_message)
		self.button.clicked.connect(self.process)

	def process(self):
		self.message.setText('start')
		self.worker.start()

	def update_message(self):
		self.message.setText('finish')
