import sys
sys.path.append('W:/develop/tdclass/lesson30')

from build_track.mvc import view
from build_track.mvc import controller
import hiero.core as hcore
import hiero.ui as hui
from PySide2 import QtWidgets


class NukeStudioContextMenu(object):
    def __init__(self):
        hcore.events.registerInterest("kShowContextMenu/kTimeline", self.timelineEventHandler)
        
    def timelineEventHandler(self, event):
        main_menu = QtWidgets.QMenu('TD Class', hui.mainWindow())
        build_track_action = QtWidgets.QAction("Build Track", hui.mainWindow())
        build_track_action.triggered.connect(self.run_build_track)
        main_menu.addAction(build_track_action)
        event.menu.addMenu(main_menu)

    def run_build_track(self):
        self.ui = view.BuildTrackDialog(hui.mainWindow())
        self.con = controller.BuildTrackController(self.ui)
        if self.con.selection:
            self.con.show_ui()

context_menu = NukeStudioContextMenu()