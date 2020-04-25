import json
import os
import shutil

import nuke

from controller import (add_gizmo, add_template, add_python, add_menu,
                        remove_item, path_join)
from controller import TOOL_ROOT, RECORD_FILE


class MenuItem(object):

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.nuke_menu = None
        self.sub_items = []
        if name != 'add item':
            self._create_add_item_menu()
            self._create_remove_item_menu()

    @property
    def path(self):
        if isinstance(self.parent, nuke.Menu):
            return path_join(TOOL_ROOT, 'tool_storage')
        return path_join(self.parent.path, self.name)

    def _check_name(self, name):
        for item in self.sub_items:
            if name == item.name:
                return False
        return True

    def add_sub_menu(self, name):
        if self._check_name(name):
            menu = MenuItem(name, self)
            self.sub_items.append(menu)
            return menu
        return None

    def add_sub_command(self, name, callback):
        if self._check_name(name):
            command = CommandItem(name, callback, self)
            self.sub_items.append(command)
            return command
        return None

    def remove(self):
        self.parent.sub_items.remove(self)
        if os.path.isdir(self.path):
            try:
                shutil.rmtree(self.path)
            except (WindowsError, IOError):
                pass

    def remove_sub_item(self, name):
        for item in self.sub_items:
            if name == item.name:
                item.remove()
                del item
                break

    def _create_add_item_menu(self):
        menu = self.add_sub_menu('add item')
        menu.add_sub_command('gizmo', lambda: add_gizmo(self))
        menu.add_sub_command('template', lambda: add_template(self))
        menu.add_sub_command('python', lambda: add_python(self))
        menu.add_sub_command('sub menu', lambda: add_menu(self))

    def _create_remove_item_menu(self):
        self.add_sub_command('remove item', lambda: remove_item(self))

    def create(self):
        if isinstance(self.parent, nuke.Menu):
            self.nuke_menu = self.parent.addMenu(self.name)
        else:
            self.nuke_menu = self.parent.nuke_menu.addMenu(self.name)
        for item in self.sub_items:
            item.create()

    def create_item(self, record):
        if record['type'] == 'menu':
            sub_menu = self.add_sub_menu(record['name'])
            for sub_item in record['sub_items']:
                sub_menu.create_item(sub_item)
        elif record['type'] == 'command':
            self.add_sub_command(record['name'],
                                 record['script'].encode('utf-8'))


class RootMenu(MenuItem):

    def __init__(self, name, parent):
        super(RootMenu, self).__init__(name, parent)

    def initialize(self):
        if os.path.isfile(RECORD_FILE):
            with open(RECORD_FILE, 'r') as f:
                data = json.load(f)
            for record in data.get('root', []):
                self.create_item(record)
            self.create()


class CommandItem(object):

    def __init__(self, name, script, parent):
        self.name = name
        self.script = script
        self.parent = parent
        self.file_path = None
        nuke.pluginAddPath(self.parent.path)

    def create(self):
        if isinstance(self.parent, nuke.Menu):
            self.parent.addCommand(self.name, self.script)
        else:
            self.parent.nuke_menu.addCommand(self.name, self.script)

    def remove(self):
        self.parent.sub_items.remove(self)
        if os.path.isfile(self.file_path):
            try:
                os.remove(self.file_path)
            except (WindowsError, IOError):
                pass


def get_menu_record(menu_item):
    record = []
    for item in menu_item.sub_items:
        if item.name in ('add item', 'remove item'):
            continue
        if isinstance(item, MenuItem):
            sub_record = get_menu_record(item)
            record.append({'name': item.name,
                           'type': 'menu',
                           'sub_items': sub_record})
        elif isinstance(item, CommandItem):
            record.append({'name': item.name,
                           'type': 'command',
                           'script': item.script})
    return record


def save_record(menu_item):
    record = get_menu_record(menu_item)
    with open(RECORD_FILE.replace('\\', '/'), 'w') as f:
        json.dump({'root': record}, f)
