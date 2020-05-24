# _*_ coding: utf-8 _*_
# @Time      : 5/23/2020 11:28 PM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : dailies_control.py
# @software  : PyCharm
import os
import re

import nukescripts

pattern = r'[\/\W:]+\/(?P<show>\W+)_(?P<sequence>\W+)_(?P<shot>\W+)_(?P<step>\W+)_(?P<version>V)'

dailies_path_pattern=('')

def dailies_control(panel,read,slate,write):
    source = read['file'].value()
    match = re.match(pattern,source)
    if match:
        source_info = match.groupdict()
        write['file'].fromUserText(dailies_path_pattern.format(**source_info))
        write['create_directories'].setValue(True)
        slate['autoShow'].setValue(False)
        slate["autoVersion"].setValue(False)
        slate['showName'].setValue(source_info['show'].upper())
        slate['versionName'].setValue(os.path.splitext(os.path.basename(write['file'].value()))[0])
        slate['format'].setValue('HD_720')
        slate['headHandle'].setValue(5)
        slate['tailHandle'].setValue(5)

    else:
        write['disable'].setValue(True)
        panel.render_infos.pop(write.name())