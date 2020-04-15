# coding=utf-8

import os

import nuke
import nukescripts

from dialog import (AddGizmoDialog, AddTemplateDialog, AddPythonDialog,
                    AddMenuDialog, RemoveItemDialog)

TOOL_ROOT = os.path.dirname(os.path.abspath(__file__))
RECORD_FILE = os.path.join(TOOL_ROOT, 'tool_storage/menu_record.json')


def path_join(*args):
    return os.path.join(*args).replace('\\', '/')


def makedirs(path):
    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))


def add_gizmo(menu_item):
    if nuke.selectedNode().Class() not in ('Group', 'Gizmo'):
        nuke.message('You should select a Group or Gizmo node.')
        return
    dialog = AddGizmoDialog()
    if dialog.exec_():
        name = dialog.name
        gizmo = nuke.selectedNode()
        nukescripts.clear_selection_recursive()
        gizmo.setSelected(True)
        if gizmo.name() != name:
            gizmo.setName('{}1'.format(name))
        gizmo_path = path_join(menu_item.path, '{}.gizmo'.format(name))
        makedirs(gizmo_path)
        nuke.nodeCopy(gizmo_path)
        command = menu_item.add_sub_command(
            name, "nuke.createNode('{}')".format(name))
        if command:
            command.file_path = gizmo_path
            command.create()


def add_template(menu_item):
    if not nuke.selectedNodes():
        nuke.message('You should select one or more nodes.')
        return
    dialog = AddTemplateDialog()
    if dialog.exec_():
        name = dialog.name
        template_path = path_join(menu_item.path,
                                  '{}.nk'.format(name.replace(' ', '_')))
        makedirs(template_path)
        nuke.nodeCopy(template_path)
        command = menu_item.add_sub_command(
            name, "nuke.scriptReadFile('{}')".format(template_path))
        if command:
            command.file_path = template_path
            command.create()


def add_python(menu_item):
    dialog = AddPythonDialog()
    if dialog.exec_() and dialog.script:
        name = dialog.name
        python_file_path = path_join(menu_item.path, '{}.py'.format(name))
        makedirs(python_file_path)
        with open(python_file_path, 'w') as f:
            f.write(dialog.script)
        cmd = ("with open('{}', 'r') as f:\n\tscript=f.readlines()\n"
               "exec(''.join(script))".format(python_file_path))
        command = menu_item.add_sub_command(name, cmd)
        if command:
            command.file_path = python_file_path
            command.create()


def add_menu(menu_item):
    dialog = AddMenuDialog()
    if dialog.exec_():
        name = dialog.name
        menu = menu_item.add_sub_menu(name)
        if menu:
            menu.create()


def remove_item(menu_item):
    item_names = []
    for item in menu_item.sub_items:
        if item.name not in ('add tool', 'remove item'):
            item_names.append(item.name)
    dialog = RemoveItemDialog(item_names)
    if dialog.exec_() and dialog.delete_names:
        for name in dialog.delete_names:
            menu_item.nuke_menu.removeItem(name)
            menu_item.remove_sub_item(name)
