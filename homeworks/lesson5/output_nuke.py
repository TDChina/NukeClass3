import nuke
import subprocess
import re
def Output(nk_file):
    write_name = []
    nuke.scriptReadFile(nk_file)
    write_list = nuke.allNodes("Write")
    startFrame = int(nuke.root()["first_frame"].value())
    print startFrame
    endFrame =  int(nuke.root()["last_frame"].value())
    print endFrame
    if not write_list:
        print "no write node to output"
        return
    write_name = [i.name() for i in write_list]
    print "select write node to output"
    print  write_name

    output_write_name = raw_input()
    if not output_write_name in write_name:
        print "has no this write node"
        return

    print "this project frame range is {}-{}".format(startFrame,endFrame)
    print "enter startframe and endframe"

    input_frame_range = raw_input()
    output_frame_range = re.findall("\d+", input_frame_range)
    print "output_frame_range {}{}".format(output_frame_range[0],output_frame_range[1])
    finalOutput_startframe = output_frame_range[0]
    finalOutput_endframe =  output_frame_range[1]
    if int(finalOutput_startframe) >= int(startFrame) and int(finalOutput_endframe) <=  int(endFrame):
        print "ok"
        cmd = "C:\\Program Files\\Nuke11.1v3\\Nuke11.1.exe --nukex -i -X " + output_write_name + ' -F "' + finalOutput_startframe+ "-" + finalOutput_endframe + '" ' + nk_file
        #print cmd
        subprocess.call(cmd)
    else:
        print "ouputFrame out of projet range"


Output("X:\\PET\\shot_work\\s074\\c0002\\cmp\work\\PET_s074_c0002_cmp_v003.nk")


