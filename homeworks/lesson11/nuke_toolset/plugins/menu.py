import os
import nuke
import types

def createMenu():
  menu = nuke.menu('Nodes')
  subMenu = menu.addMenu("GR_Noise")
  subMenu.addCommand('GR_Noise', 'nuke.createNode("GR_Noise")')

createMenu()