import sys
sys.path.append('W:/develop/tdclass')

from Qt import QtWidgets

from batch_transcoder.frontend.mvc.controller import BatchTranscoderController
from batch_transcoder.frontend.mvc.view import BatchTranscoderUI


app = QtWidgets.QApplication(sys.argv)
view = BatchTranscoderUI()
c = BatchTranscoderController(view)
c._view.show()
sys.exit(app.exec_())
