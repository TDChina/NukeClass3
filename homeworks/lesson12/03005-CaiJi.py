#!/usr/bin/env python
#_*_coding:utf-8_*_


import nuke

for i in ['command1','command2','command3']:
    nuke.menu("Node Graph").addCommand(i,"nuke.message('%s')"%i)
