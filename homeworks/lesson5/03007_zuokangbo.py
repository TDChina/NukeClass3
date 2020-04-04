# _*_ coding: utf-8 _*_
# @Time      : 3/31/2020 11:22 PM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : 03007_zuokangbo.py
# @software  : PyCharm
import os
import re

###### You can set nuke's path as an environment variable
def get_nuke_path_en():
    '''get nuke environ path'''
    nuke_path_en = os.environ.get('NUKE_PATH',None)

    return nuke_path_en

def nuke_export(nuke_path_en = get_nuke_path_en()):
    '''nuke file render export'''
    if not nuke_path_en:
        print("NUKE_PATH failed to get:\n")
        nukePath = get_nuke_path()
        render_line_list = nuke_export_set(nukePath)
        if render_line_list:
            nuke_export_mode(render_line_list)
    else:
        render_line_list = nuke_export_set(nuke_path_en)
        if render_line_list:
            nuke_export_mode(render_line_list)

def nuke_export_mode(render_line_list):
    '''
    Save bat file or not
    '''
    select_model = input('select export model:\n1.save bat file to disk\n2.Run directly at the terminal\n')
    if select_model == '1':
        export_bat_file(render_line_list)
        return 1
    if select_model == '2':
        for render_line in render_line_list:
            os.popen(render_line)
        return 1
    else:
        print("Wrong information entered!!")
        return 0

def export_bat_file(render_line_list):
    '''export bat file to hard disk'''
    bat_path = input("Input Bat save file path:\n")
    if os.path.isdir(bat_path):
        bat_name = input("Bat file name:\n")
        bat_echo = '@echo off\ncolor 17\necho --------------------\necho Number of nuke files to render(%s)\npause\n' %len(render_line_list)
        f = open('/'.join(bat_path.split('\\'))+'/%s.bat' %bat_name,'a')
        f.write(bat_echo)
        for line in render_line_list:
            f.write(line+"\n")
        f.close()
        print('export success %s' %bat_path)
        return 1
    else:
        print('Wrong file path!!')
        return 0

def nuke_export_set(nukePath = None):
    'nuke_export value set'
    if nukePath:
        frame_range_list = frame_range()
        nuke_file_path = get_nuke_file()
        write_name_list = export_write_name()
        if (frame_range_list and nuke_file_path and write_name_list):
            if not len(write_name_list)>1:
                render_line_list = []
                for frame in frame_range_list:
                    render_line = render_com(nukePath, frame, write_name_list[0], nuke_file_path)
                    render_line_list.append(render_line)
                return render_line_list
            else:
                if (len(frame_range_list) == len(write_name_list)):
                    render_line_list = []
                    for i in range(len(frame_range_list)):
                        render_line = render_com(nukePath, frame_range_list[i], write_name_list[i], nuke_file_path)
                        render_line_list.append(render_line)
                        return render_line_list
                else:
                    print("frame range count and write count not equal")
                    return 0
        else:
            return 0
    else:
        return 0

def get_nuke_path():
    '''get nuke path'''
    nukePath = input('Please input nuke path:')
    ext = os.path.exists(nukePath)
    if not ext:
        # if the extension is not *.exe
        print('Error:Please select the suffix with EXE nuke program to complete the path')
        return 0
    else:
        return nukePath

def frame_range():
    '''get export frame range list'''
    get_frame_range = input('Input export frame range,if it is a multi segment range, please separate it with "," :\n')
    frame_range_list = str(get_frame_range).split(',')
    for i in frame_range_list:
        isnumber = re.compile(r"(^\d+\-\d+$)|(\d+$)").match(i)
        if not isnumber:
            print("Input format error")
            return 0
    return frame_range_list

def export_write_name():
    '''get write name list'''
    input_write = input('Enter a write name. Separate multiple names with ",":\n')
    write_list = input_write.split(',')
    for i in write_list:
        isalphas = i.isalnum()
        if not isalphas:
            print("Input format error")
            return 0
    return write_list

def get_nuke_file():
    '''get nuke file path'''
    input_nk_file = input("Please enter nuke project file path:\n")
    ext = os.path.exists(input_nk_file)
    if not ext:
        print("The entered file path is incorrect")
        return 0
    else:
        return input_nk_file

def render_com(nuke_path,frame,write_name,nuke_file_path):
    '''render line'''

    batch_render = '"'+r"%s" %nuke_path +'"'+ ' -x '+"-F %s"%frame + ' -X '+"%s"%write_name + ' --cont ' + '"'+r"%s" %nuke_file_path + '"'
    return batch_render


if __name__ == '__main__':
    nuke_export()
