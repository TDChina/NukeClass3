# -*- coding: utf-8 -*-
# .@FileName:script_update
# @Date....:2020-04-04  20:49   
# ..:XingLian
import re
import nuke
import nukescripts

# 获取工程名称
script_name = nuke.scriptName()
# 匹配是否存在版本号，如果不存在，另存为版本1，并进行升级操作
if not re.search(script_name, r'.?_v/d*.nk$'):
    print re.search(script_name, r'.?_v/d*.nk$')
    new_script_name = script_name[::-1].replace('kn.', 'kn.100v_', 1)[::-1]
    print new_script_name
    nuke.scriptSaveAs(new_script_name)
nukescripts.script_and_write_nodes_version_up()