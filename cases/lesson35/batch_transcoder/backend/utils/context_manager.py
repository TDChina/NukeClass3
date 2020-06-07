import importlib
import sys


class SysPath(object):
    def __init__(self, path):
        self.path = path
        self.original_sys_path = []

    def __enter__(self):
        self.original_sys_path = sys.path[:]
        sys.path = [self.path]

    def __exit__(self, exc_type, exc_value, traceback):
        sys.path = self.original_sys_path


def get_module(name, path):
    with SysPath(path):
        module = importlib.import_module(name)
    return module
