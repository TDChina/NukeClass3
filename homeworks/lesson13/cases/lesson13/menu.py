# coding=utf-8

import nuke

from menu_creator import RootMenu, save_record

# Set the name and type of menu
toolkit_menu = RootMenu('Toolkit', nuke.menu('Nuke'))

toolkit_menu.initialize()

# addOnScriptClose add code to execute before a script is closed

nuke.addOnScriptClose(save_record, args=(toolkit_menu,))
