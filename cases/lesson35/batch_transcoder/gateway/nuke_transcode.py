import os
import subprocess

NUKE_EXE = 'C:/Program Files/Nuke11.3v5/Nuke11.3.exe'
PYTHONPATH = 'W:/develop/tdclass/nuke_env'
NUKE_PATH = 'W:/develop/tdclass/nuke_env'


def run_nuke_transcode(template_file):
    cmd = [NUKE_EXE, '-xi', template_file]
    os.environ['NUKE_PATH'] = NUKE_PATH
    os.environ['PYTHONPATH'] = PYTHONPATH
    return subprocess.check_call(cmd, env=os.environ)
