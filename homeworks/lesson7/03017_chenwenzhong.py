# coding:utf-8
import nuke
import os

# sequence fromat list
sequence_file = ['dpx', 'exr', 'jpeg', 'jpg', 'hdr', 'png', 'tif', 'tiff', 'tga'， 'mov']


def get_frame_range(read_list):
    """
    get the start and end frames from the read file if the read is a sequence
    :param read_list: the path of read file
    :return: Start and end frames of the sequence
    """
    for i in read_list:
        # print i
        split_path = i.split('/')
        # print split_path
        seq_path = split_path[-1]
        # print seq_path
        medie_path = '/'.join(split_path[:-1])
        # print medie_path
        dir_name = os.listdir(medie_path)
        first_frame = dir_name[0].split('.')[-2]
        last_frame = dir_name[-1].split('.')[-2]

        return first_frame, last_frame


def main(read_path):
    """
    create the Read node and get the file value from the read file
    :param read_path: the read file path
    :return: None
    """
    for seq in read_path:
        splitpath = seq.split('/')
        damedia = splitpath[-1]
        seq_format = damedia.split('.')[-1]
        # print splitpath
        # print damedia
        # print seq_format
        # whether the sequence format is in the sequence_list
        if seq_format in sequence_file:
            # if it is a sequence
            if not damedia.find('%') == -1:
                print damedia + ' is a sequence'
                # deal with the sequence and get the start and end frames
                first_frame, last_frame = get_frame_range(read_list)
                read_node = nuke.createNode('Read')
                read_node['file'].setValue(seq)
                read_node['first'].setValue(int(first_frame))
                read_node['last'].setValue(int(last_frame))
                read_node['origfirst'].setValue(int(first_frame))
                read_node['origlast'].setValue(int(last_frame))

            # it's a mov
            elif damedia.find('mov') != -1:
                print damedia + ' is mov'
                nuke.createNode('Read')['file'].fromUserText(seq)

            # if it is a still image get the file value
            else:
                print damedia + ' is a still image'
                read_node2 = nuke.createNode('Read')
                read_node2['file'].setValue(seq)
        else:
            print 'The sequence foramat is incorrect'


if __name__ == '__main__':
    read_list = ['E:/matchmove_source/Space Cop_2/Space Cop_2.####.jpg',
                 'E:/matchmove_source/still_frame/delivery.0021.jpg']

    main(read_list)


