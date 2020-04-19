print 'userA`s tools is load'

import os
import sys

import nuke

NUKE_PATH = os.environ.get('NUKE_PATH')
nuke.pluginAddPath(os.listdir(NUKE_PATH))