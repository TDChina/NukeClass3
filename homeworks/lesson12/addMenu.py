# _*_ coding: utf-8 _*_
# @Time      : 4/19/2020 12:58 AM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : addMenu.py
# @software  : PyCharm

com = ['command1', 'command2', 'command3']

def addmenus(com):
    menus = nuke.menu('Node Graph')
    menusList = menus.addMenu('testCommand')
    for name in com:
        comLine = lambda name: 'nuke.message(' + "'" + '%s' % name + "'" + ')'
        LineName = comLine(name)
        menusList.addCommand('%s' % name, LineName)

addmenus(com)