#!/usr/bin/env python
#_*_coding:utf-8_*_

import os
import nuke


def new_read(path):

    if not os.path.isdir(path):
        nuke.message("This is not a path")
        return

    file_list = nuke.getFileNameList(path)

    if not file_list:
        nuke.message("No file at this path")
        return

    suffix_list = [".mov",".jpg",".png",".exr"]


    for i in file_list:
        if os.path.splitext(i)[1].lower() in suffix_list:

            new_image_or_mov_read(os.path.join(path,i))


        else:
            sequence = i.split(" ")
            if os.path.splitext(sequence)[1].lower() in suffix_list:
                new_sequence_rad(os.path.join(path,sequence[0]) , sequence[1])



def new_image_or_mov_read(path):

    read_value = "file {" + path + "}"
    nuke.createNode("Read",read_value)


def new_sequence_rad(path,frame_range):
    first,last = frame_range.split("-")

    read_value = "file {%s} first %s last %s" % (path,first,last)
    nuke.createNode("Read",read_value)






new_read("D:\\cs")

