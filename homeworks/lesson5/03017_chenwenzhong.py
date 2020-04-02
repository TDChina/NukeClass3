#coding:utf-8
import nuke
import re
import subprocess

'''
This is a tool for user-defined write nodes! User can enter write node and selected range of rendering frames!
'''

# input a nuke file       
nuke_file = raw_input('Please enter a nuke file:')

# open the file
nk_file = nuke.scriptReadFile(nuke_file)

# get write nodes
write_node_list = list()
for node in nuke.allNodes():
    if node.Class() == 'Write':
        write_node_list.append(node.name())
    # else:
    #     print 'The project has no write nodes' 

print write_node_list

# no write node
if write_node_list == []:
    print 'The project has no write nodes'

# user input write node
while True:
    user_input = raw_input('Input write node name:')
    if user_input not in write_node_list:
        print('no write node in list ')   
    else:
        break

    
# get the framerange

first_frame = int(nuke.Root()['first_frame'].value())
last_frame = int(nuke.Root()['last_frame'].value())

# frame_range 
print('The frame_range is:%d-%d' % (first_frame, last_frame))

# enter the render framrange
render_framerange = raw_input('Plz enter the renderframrange:')

user_enter_framerange = re.match(r"[0-9]+-[0-9]+", render_framerange)
if user_enter_framerange:
    ret_framerange = user_enter_framerange.group()
else:
    print 'Out of frame, please re-enter!'
    

a = 'C:/Program Files/Nuke11.3v3/Nuke11.3.exe --nukex -i -X {} -F {} {}'.format(user_input, ret_framerange, nuke_file)

subprocess.call(a)

