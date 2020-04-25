#!/usr/bin/env python
#_*_coding:utf-8_*_

import nuke
import os
import re


def main(path):

    read_list = nuke.getFileNameList(path,True,True,False)

    if not read_list:
        nuke.message("The path does not exist or there is no file in the path")
        return

    for file_name in read_list:

        if re.search("\d+-\d+",file_name) == None:
            continue

        read = nuke.createNode("Read","file {%s}"%os.path.join(path,file_name))

        reformat = nuke.createNode("Reformat","format HD_720")
        reformat.setInput(0,read)

        mov_name = re.match(".+?\.",file_name).group() + "mov"
        write = nuke.createNode("Write","file {%s}"%os.path.join(path,mov_name))
        write["mov64_fps"].setValue(24.0)
        write["meta_codec"].setValue("avc1")

        nuke.render(write,read["first"].value(),read["last"].value())


if __name__ == "__main__":

    main("D:\cs")


