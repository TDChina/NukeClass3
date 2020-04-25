import nuke


def main(file_folder):

    # get the all sequence in the folder
    file_list = nuke.getFileNameList(file_folder)
    if not file_list:
    	nuke.message('no seq in this folder')
    for seq in file_list:
        seq_name = seq.split(' ')[0]
        frame_range = seq.split(' ')[-1]
        first_frame = frame_range.split('-')[0]
        last_frame = frame_range.split('-')[1]

    # create read node
    
    read_node = nuke.createNode('Read')
    read_node['file'].fromUserText(file_folder + '/' + seq)
    read_node.setXYpos(100, 200)

    # create reformat and set size
    reformat_node = nuke.createNode('Reformat')
    reformat_node['format'].setValue('HD_720')
    reformat_node.setXYpos(read_node.xpos(), read_node.ypos()+100)
    
    # create write node
    write_node = nuke.createNode('Write')
    write_node['file'].setValue(file_folder + '/' + seq_name + '.mov')
    write_node['meta_codec'].setValue('avc1')
    write_node['mov64_fps'].setValue(24)
    write_node.setXYpos(reformat_node.xpos(), reformat_node.ypos()+100)
    nuke.render(write_node, first_frame, last_frame)
    

if __name__ == '__main__':
	main('E:/matchmove_source/Space Cop_2')