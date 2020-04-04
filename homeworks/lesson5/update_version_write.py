# coding:utf-8
import nuke
import os
import re
import subprocess

"""
This is a tool for user-defined write nodes! User can enter write node and selected range of rendering frames!
"""


def get_write_node(open_file, write_node):
    """
    get all of write nodes and determine whether the input write node is in the project write node list.
    :param open_file: nuke script
    :param write_node: user enter write node
    :return: write_node ---> str
    """

    # get all of write nodes list
    write_node_list = list()
    for node in nuke.allNodes():
        if node.Class() == 'Write':
            write_node_list.append(node.name())

    # print write nodes
    print 'The project include write nodes：%s ' % write_node_list

    # if no write node
    if write_node_list is []:
        print 'The project has no write nodes'

    # user enter write node in the list or not
    if write_node in write_node_list:
        return write_node
    else:
        print('no write node in list ')


def input_frame_range(open_file, render_range):
    """
    get nuke project frame range and determine whether the input frame range meets the requirements.
    :param open_file: nuke script
    :param render_range: user enter the frame range
    :return: user_enter ---> str
    """
    # get the framerange
    first_frame = int(nuke.Root()['first_frame'].value())
    last_frame = int(nuke.Root()['last_frame'].value())
    # frame_range
    print('The frame_range is:%d-%d' % (first_frame, last_frame))

    # determine whether the frame range is requirement, it can enter multiple.
    user_enter = re.findall(r"[0-9]+-[0-9]+", render_range)

    if user_enter:
        # The last frame is biger than the previous frame.
        element = render_range.split(' ')
        num_list = list()
        for frame in element:
            nums = frame.split('-')
            if int(nums[0]) < int(nums[1]):
                pass
            else:
                print 'the frame you entered is incorret'
            for num in nums:
                num_list.append(num)

        # if out of frame
        if int(num_list[-1]) > last_frame:
            print 'Out of frame, please re-enter!'

        return ' '.join(user_enter)
    else:
        print 'Plz enter again!'



def seleted_write(nuke_file, write_node, render_range):
    """
    Main function to execute!
    :param nuke_file: nuke script full path
    :param write_node: user entered write node
    :param render_range: user entered frame range
    :return: None
    """
    # determine whether the nuke script file is exists
    if os.path.exists(nuke_file):
        open_file = nuke.scriptReadFile(nuke_file)
    else:
        print 'The project does not exists'

    input_write_node = get_write_node(open_file, write_node)
    frame_range = input_frame_range(open_file, render_range)

    retsult = 'C:/Program Files/Nuke11.3v3/Nuke11.3.exe --nukex -i -X {} {}'.format(input_write_node, nuke_file)\
              + " " + frame_range
    print retsult

    subprocess.call(retsult)


seleted_write('E:/write_test_v01.nk', 'Write2', '32-33 40-44 75-76')