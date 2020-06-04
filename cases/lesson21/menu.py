from auto_write_path import auto_write_path

from config import path_pattern, task_names, write_path_pattern

nuke.menu('Nodes').addCommand('Custom/auto_write_path', "auto_write_path(path_pattern, task_names, write_path_pattern)")