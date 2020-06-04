import nuke

from slate_knob_changed import *

from dailies_render import DailiesSettingPanel
from dailies_control import dailies_control

dailies_command = """
import thread
dailies_panel = DailiesSettingPanel()
dailies_panel.register_control(dailies_control)
dailies_panel.show()
"""

nuke.menu('Nodes').addCommand('Custom/Dailies', dailies_command)