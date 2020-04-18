# _*_ coding: utf-8 _*_
# @Time      : 4/18/2020 12:30 AM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : load_tools.py
# @software  : PyCharm

import os
import subprocess
import yaml

def runMain():
    '''get config file'''

    with open('D:/my_script/NukeClass3/homeworks/lesson11/configFile.yaml','r') as f:
        data = yaml.load(f, Loader = yaml.FullLoader)
    nukePath = runNukeVersion(data)
    if nukePath:
        loadPlugins(data,nukePath)

def runNukeVersion(data):
    '''get nuke run path'''
    nukeAllVersion = []
    count = 1
    for nukeVersion in data["SoftWare"]:
        VersionNum = nukeVersion['nukeversion']
        nukeAllVersion.append(VersionNum)
        count += 1
    startup_nuke = input('Please select the version to start:\n'+str(nukeAllVersion)+"\n")

    try:
        num = float(startup_nuke)
        if num in nukeAllVersion:
            for x in data["SoftWare"]:
                if x["nukeversion"] == num:
                    nuke_path = x['path']
                    break
            return nuke_path, num
        else:
            print("Please enter a version that exists in the list:->"+str(nukeAllVersion))
            return False
    except ValueError:
        print("Please enter version number:The ->'%s'<- you entered is illegal" %startup_nuke)
        return False

def loadPlugins(data,nukePath):

    pluginsPath = data['nuke_toolPath']
    env_ = os.environ.copy()

    for p in data['plugins']:
        if p['version']:
            if "NUKE_PATH" in env_:
                env_['NUKE_PATH'] = os.path.join(pluginsPath,p['value'])+';'+env_['NUKE_PATH']
            else:
                env_['NUKE_PATH'] = os.path.join(pluginsPath, p['value']).replace('.', '_')
        else:
            if "NUKE_PATH" in env_:
                env_['NUKE_PATH'] = os.path.join(pluginsPath, p['value'])+';'+ env_['NUKE_PATH']
            else:
                env_['NUKE_PATH'] = os.path.join(pluginsPath, p['value'])
                print('loading plugin %s success' %p['name'])

    for g in data['gizmos']:
        env_['NUKE_PATH'] = os.path.join(pluginsPath, g['value'])+';'+ env_['NUKE_PATH']
        print('loading gizmos %s success' % g['name'])

    pathonScript = data['python'][0]['value']
    env_['NUKE_PATH'] = os.path.join(pluginsPath, pathonScript)+';'+ env_['NUKE_PATH']
    print('loading python script success')

    ofxPlugin = data['ofx'][0]['value']
    env_['OFX_PLUGIN_PATH'] = os.path.join(pluginsPath, ofxPlugin)
    print('loading ofx script success')

    subprocess.Popen("%s" %nukePath[0], env = env_)


if __name__ == '__main__':
    runMain()