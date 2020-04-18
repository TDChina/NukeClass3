## init.py
## loaded by nuke before menu.py

nuke.pluginAddPath('labelAutobackdrop')
nuke.pluginAddPath('autoCrop')
nuke.pluginAddPath('autoContactSheet')

nuke.pluginAddPath('testLoad')
import testLoad
testLoad.loadPluginsInfo()