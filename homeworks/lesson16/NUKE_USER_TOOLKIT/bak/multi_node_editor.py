# _*_ coding: utf-8 _*_
# @Time      : 5/2/2020 10:52 PM
# @author    : zuokangbo
# @eamil     : 1156298563@qq.com
# @File      : multi_node_editor.py
# @software  : PyCharm

import nuke

class MultiNodeEditor():

    def __init__(self):
        # 获取当前节点，用类变量保存,返回NoOp节点上所有的控件包括值
        self.editor = nuke.thisNode()
        # 需要获取需要接管的节点列表
        self.all_nodes = []

    def get_nodes(self):

        # 获取noOp自定义控件class中输入的值
        node_class = self.editor['class'].value()
        # 获取noOp自定义控件node_name中输入的值
        node_name = self.editor['node_name'].value()
        if not node_class:
            nuke.message('You should input a node class name.')
            return 0
        # 获取nuke中所有的节点，然后遍历符合输入的类型的节点 和 节点名称的节点（模糊名称）
        all_nodes = [node for node in nuke.allNodes() if node.Class() == node_class and node_name in node.name()]
        # 判断all_nodes节点是否为空
        if not all_nodes:
            nuke.message('No valid node could be found.')
            return 0
        # 对节点进行排序（按照名称正向递增排序）
        all_nodes.sort(key = lambda x: x.name())
        self.all_nodes = all_nodes

    def get_knobs(self,mode):
        # 定义存储控件的列表
        knobs = []
        # 获取自定义控件knob_name中输入的值，并且用号分割
        knob_names = self.editor['knob_name'].value().split(',')
        # 如果mode为sync执行
        if mode == 'sync':
            for name in knob_names:
                # 判断接收到的控件名称是否合法，knobs().keys()返回该节点的所有控件名称
                if name in self.all_nodes[0].knobs().keys():
                    # 把合法的控件名称加入knobs列表中，得到需要编辑的控件名称
                    knobs.append(self.all_nodes[0].knob(name))
                else:
                    nuke.message('Can not find {} in {}.'.format(name,self.all_nodes[0].name()))
                    return 0

        elif mode == 'non sync':
            for node in self.all_nodes:
                node_knobs = []
                for name in knob_names:
                    if name in node.knobs().keys():
                        #把合法的节点控件的对象添加到列表中
                        node_knobs.append(node.knob(name))
                    else:
                        nuke.message('Can not find {} in {}.'.format(name,node.name()))
                        return []
                knobs.append(node_knobs)
        return knobs

    def add_knobs(self,mode):

        self.remove_knobs()
        custom_knob_names = []
        if mode == 'sync':
            for node in self.all_nodes:
                print(node.name())
                # 获取选择的节点的boolean，目的是让他在节点面板中显示复选框
                name_knob = nuke.Boolean_Knob(node.name())
                # 设置控件为选中状态
                name_knob.setValue(1)
                # 这里让第一个复选框另起一行，后续的就不用，可以判断自定义的控件是否存在
                if not custom_knob_names:
                    # 这里的把转换的boolean控件设置一个flag另起一行，传入nuke的一个常量，nuke.STARTLINE，引入一个控件
                    name_knob.setFlag(nuke.STARTLINE)
                self.editor.addKnob(name_knob)
                custom_knob_names.append(name_knob.name())
                # 这里的ENDLINE常量表明这一行已经结束。
            name_knob.setFlag(nuke.ENDLINE)

            for knob in self.knobs:
                self.editor.addKnob(knob)
                # 由于是同步操作，这里的knob所以节点都有，直接添加到后面
                custom_knob_names.append(knob.name())
            # 添加一个按钮，点击更新数据。
            update_knob = nuke.PyScript_Knob('update','set all values')
            update_knob.setFlag(nuke.STARTLINE)
            update_knob.setCommand('MultiNodeEditor.set_all_values()')
            self.editor.addKnob(update_knob)
            custom_knob_names.append(update_knob.name())
            print(custom_knob_names)

        elif mode == 'non sync':
            for i in range(len(self.all_nodes)):
                name_knob = nuke.Boolean_Knob(self.all_nodes[i].name())
                name_knob.setValue(1)
                name_knob.setFlag(nuke.STARTLINE)
                self.editor.addKnob(name_knob)
                custom_knob_names.append(name_knob.name())
                for knob in self.knobs[i]:
                    self.editor.addKnob(knob)
                    custom_knob_names.append(knob.name())

        self.editor['custom_knobs'].setValues(custom_knob_names)

    @staticmethod
    def set_all_values():
        editor = nuke.thisNode()
        nodes = []
        knobs = []
        for i in range(editor['custom_knobs'].numValues()):
            name = editor['custom_knobs'].enumName(i)
            if not name or name == 'update':
                continue
            knob = editor[name]
            if isinstance(knob,nuke.Boolean_Knob):
                if knob.value():
                    with nuke.Root():
                        nodes.append(nuke.toNode(name))
                else:
                    continue
            else:
                knobs.append(knob)

        for node in nodes:
            for knob in knobs:
                node[knob.name()].setValue(knob.value())


    @staticmethod
    def remove_knobs():
        editor = nuke.thisNode()
        for i in range(editor['custom_knobs'].numValues()):
            name = editor['custom_knobs'].enumName(i)
            if name:
                editor.removeKnob(editor.knob(name))
        editor['custom_knobs'].setValues([])

    def run(self):

        self.get_nodes()
        if self.all_nodes:
            # 获取自定义控件mode的值
            mode = self.editor['mode'].value()
            self.knobs = self.get_knobs(mode)
            if not self.knobs:
                return 0
            self.add_knobs(mode)