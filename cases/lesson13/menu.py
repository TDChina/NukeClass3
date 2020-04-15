# coding=utf-8

import nuke

from menu_creator import RootMenu, save_record


toolkit_menu = RootMenu('Toolkit', nuke.menu('Nuke'))
toolkit_menu.initialize()
nuke.addOnScriptClose(save_record, args=(toolkit_menu,))
