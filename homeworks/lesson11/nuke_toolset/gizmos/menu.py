import os
import sys
import nuke

# AP definitions

toolbar = nuke.menu('Nodes')
AMenu = toolbar.addMenu('Additive')
AMenu.addCommand('AdditiveKeyer', 'nuke.createNode("AdditiveKeyer")')

AMenu = toolbar.addMenu('Despill')
AMenu.addCommand('Despill', 'nuke.createNode("Despill")')