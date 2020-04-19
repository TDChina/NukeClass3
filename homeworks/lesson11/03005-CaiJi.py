#!/usr/bin/env python
#_*_coding:utf-8_*_

NUKE_TOOL_PATH = "D:/TD/NukeClass3/homeworks/lesson11/nuke_toolset"

Projects = {
    "Project 1" : ["ofx","python","plugins"],
    "Project 2" : ["ofx","python","gizmos"],
    "Project 3" : ["ofx","python","plugins","gizmos"]
}




import os
import nuke



def set_ofx_path(ofx_path):

    if "OFX_PLUGIN_PATH" in os.environ:
        os.environ["OFX_PLUGIN_PATH"] = os.environ["OFX_PLUGIN_PATH"] + "," + ofx_path
    else:
        os.environ["OFX_PLUGIN_PATH"] = ofx_path



def load_py(py_path):

    for dir , _ , file_name_list in os.walk(py_path):
        for file_name in file_name_list:
            if os.path.splitext(file_name)[1].lower() == ".py":
                nuke.pluginAddPath(dir)
                __import__(os.path.splitext(file_name)[0])



def load_dll_plugins(dll_dir):

    for dir , _ , file_name_list in os.walk(dll_dir):
        for file_name in file_name_list:
            if os.path.splitext(file_name)[1].lower() == ".dll":
                if is_load(os.path.join(dir,file_name)):

                    nuke.pluginAddPath(dir)
                    if not "menu.py" in os.listdir(dir):
                        dll_name = os.path.splitext(file_name)[0]
                        nuke.menu("Nodes").addMenu("plugins").addMenu("dll").addCommand(dll_name,"nuke.createNode('%s')" % dll_name)



def is_load(plugin_file_name):
    try:
        nuke.load(plugin_file_name)
    except Exception as e:
        nuke.error("Plugin %s cannot be loaded ,error: %s"%(plugin_file_name,str(e)))
        return False
    else:
        return True



def load_gizmos(gizmos_path):
    if "init.py" in os.listdir(gizmos_path) or "menu.py" in os.listdir(gizmos_path):
        nuke.pluginAddPath(gizmos_path)
    else:
        for i in os.listdir(gizmos_path):
            if os.path.isdir(os.path.join(gizmos_path,i)):
                load_gizmos(os.path.join(gizmos_path,i))
            else:
                if os.path.splitext(i)[1].lower() == ".gizmo":
                    nuke.pluginAddPath(gizmos_path)
                    gizmos_name = os.path.splitext(i)[0]
                    nuke.menu("Nodes").addMenu("plugins").addMenu("gizmos").addCommand(gizmos_name, "nuke.createNode('%s')" % gizmos_name)



def main(Project_name):
    if not Project_name in Projects:
        nuke.message("No project name")
        return

    for i in Projects[Project_name]:

        plugins_list[i](os.path.join(NUKE_TOOL_PATH,i))



plugins_list = {
    "ofx": set_ofx_path,
    "plugins": load_dll_plugins,
    "python": load_py,
    "gizmos": load_gizmos
}


if __name__ == "__main__":

    main("Project 3")

