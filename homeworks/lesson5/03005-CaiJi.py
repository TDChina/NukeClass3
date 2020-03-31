#!/usr/bin/env python
#_*_coding:utf-8_*_



import nuke
import subprocess
import re


def Render_Write(nk_file):
    nuke.scriptReadFile(nk_file)

    write_list = nuke.allNodes("Write")

    if not write_list:
        print "This file has no Write node"
        return

    write_name_list = [i.name() for i in write_list]

    print
    print "This file contains the following write nodes:"
    print write_name_list
    print "Enter the name of the write node to be rendered:"
    print
    in_write_name = raw_input()
    if not in_write_name in write_name_list:
        print "Without this write node"
        return

    print
    print "The frame range of this project is: " + str(int(nuke.root()["first_frame"].value())) + "-" + str(int(nuke.root()["last_frame"].value()))
    print "Input rendering frame range, start-end, Separate multiple frame ranges with spaces"
    print

    in_frame_range = raw_input()



    frame_range_list = re.findall("\d+-\d+",in_frame_range)

    if not frame_range_list:
        print "No canonical frame range"
        return

    frame_range =" ".join(frame_range_list)


    cmd = "C:\\Program Files\\Nuke11.2v3\\Nuke11.2.exe --nukex -i -X " + in_write_name + ' -F "' + frame_range + '" ' + nk_file


    subprocess.call(cmd)


Render_Write("C:\\Users\\Alienware\\Desktop\\aaa_V001.nk")



