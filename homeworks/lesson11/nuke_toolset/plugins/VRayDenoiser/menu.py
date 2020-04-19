import os
import nuke
import types

def createMenu():
  menu = nuke.menu('Nodes')
  subMenu = menu.addMenu("V-Ray Tools", icon = "VRayTools.png")
  subMenu.addCommand('VRayDenoiser', 'nuke.createNode("VRayDenoiser")', icon = "VRayDenoiser.png")

createMenu()