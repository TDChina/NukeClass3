# _*_ coding: utf-8 _*_
# @Time      : 4/18/2020 9:43 PM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : testLoad.py
# @software  : PyCharm
import nuke

def loadPluginsInfo():
    pluginsList = ["A_ChannelManager", 'AdditiveKeyer', 'Despill', 'VRayDenoiser', 'ColorCarpet', 'GR_Noise']
    count = 0
    for i in pluginsList:
        info = pluginexists(i)
        print(str(count)+'--'+i+':'+info)
        count +=1

def pluginexists(plugName):
    loadJudge = nuke.pluginExists('%s' %plugName)
    if loadJudge:
        loadInfo = 'Load successful'
    else:
        loadInfo = 'Load failure'
    return loadInfo

if __name__ == '__main__':
    loadPluginsInfo()