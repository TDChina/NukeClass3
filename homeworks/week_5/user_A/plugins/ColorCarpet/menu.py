"""Add the node to Nuke's UI."""

# Import built-in modules
import os
import platform

# Import third-party nodes
import nuke  # pylint: disable=import-error


def add_plugin():
    """Add the os- and variant specific node to Nuke's plugin path."""
    version = "{}_{}".format(nuke.NUKE_VERSION_MAJOR, nuke.NUKE_VERSION_MINOR)
    path = os.path.join(os.path.dirname(__file__), platform.system(), version)
    path = path.replace("\\", "/")
    path = os.path.abspath(path)
    nuke.pluginAddPath(path)


def add_to_ui():
    """Add the node to Nuke's UI."""
    menu = nuke.menu("Nodes").addMenu("Leafpictures", icon="leafpictures.png")
    menu.addCommand("l_ColorCarpet", "nuke.createNode('ColorCarpet')",
                    icon="ColorCarpet.png")


add_plugin()
add_to_ui()
