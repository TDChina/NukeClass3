import os
import sys
import nuke

# AP definitions

toolbar = nuke.menu('Nodes')
AMenu = toolbar.addMenu('AP', icon='AP.png')
AMenu.addCommand('A_ChannelManager', 'nuke.createNode("A_ChannelManager")', icon='AP.png')