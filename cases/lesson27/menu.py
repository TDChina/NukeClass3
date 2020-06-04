import nuke

from view import PackageToolUI

from controller import NukePackageController

ui = PackageToolUI()

controller = NukePackageController(ui)

nuke.menu('Nodes').addCommand('Custom/Packaging', 'controller.view.show()')