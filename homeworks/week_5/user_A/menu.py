import nuke
if len(nuke.pluginPath(0)) == len(nuke.pluginPath(1)):
    print u'plugins all load'

for i in range(1, 4):
    command = 'lambda: nuke.message("Command{}")'.format(i)
    nuke.menu('Node Graph').addCommand('Command{}'.format(i), eval(command))

