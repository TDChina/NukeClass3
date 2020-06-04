import os
import shutil

from PySide2 import QtCore

from model import NukePackageWrapper
import utils


class CollectThread(QtCore.QThread):
    finish = QtCore.Signal()
    def __init__(self, dest_root):
        super(CollectThread, self).__init__()
        self.package_wrapper = None
        self.dest_root = dest_root
        self.run_flag = True
        self.index = 0
        self.log = []

    def run(self):
        self.package_wrapper = NukePackageWrapper(self.dest_root)
        while self.run_flag and self.index < len(self.package_wrapper.nodes):
            self.package_wrapper.grab_source(self.index)
            self.index += 1
        if self.package_wrapper.error_nodes:
            self.log.append('\n\nNodes with error:')
        for node in self.package_wrapper.error_nodes:
            self.log.append('\n{}'.format(node.name()))
        self.finish.emit()

class SingleCopyThread(QtCore.QThread):
    finish = QtCore.Signal()
    copy_one_file = QtCore.Signal(str)
    def __init__(self, source_list, dest_folder):
        super(SingleCopyThread, self).__init__()
        self.source_list = source_list
        self.dest_folder = '{}/sources'.format(dest_folder)
        self.run_flag = True
        self._mutex = QtCore.QMutex()
        self.log = []

    def run(self):
        source_count = len(self.source_list)
        copy_count = 0
        source_iter = iter(self.source_list)
        while self.run_flag and copy_count < source_count:
            node_name, source = source_iter.next()
            shutil.copy2(source, self.dest_folder)
            self._mutex.lock()
            self.copy_one_file.emit(source)
            self.log.append('\n\n{}\n{}'.format(node_name, source))
            self._mutex.unlock()
            copy_count += 1
        self.finish.emit()

class SequenceCopyThread(QtCore.QThread):
    finish = QtCore.Signal()
    copy_one_file = QtCore.Signal(str)

    def __init__(self, basename, sequence_info, dest_folder):
        super(SequenceCopyThread, self).__init__()
        self.node_name = sequence_info[0]
        self.source_files = sequence_info[1]
        self.first = sequence_info[2]
        self.last = sequence_info[3]
        self.basename = basename
        self.dest_folder = '{}/sources/{}'.format(dest_folder, basename)
        self.run_flag = True
        self._mutex = QtCore.QMutex()
        self.log = []
        self.index = 0

    def run(self):
        sequence_length = len(self.source_files)
        if sequence_length < self.last - self.first + 1:
            self.log.append('\n\n{} (missing frame)'.format(self.node_name))
        else:
            self.log.append('\n\n{}'.format(self.node_name))
        if not os.path.isdir(self.dest_folder):
            os.makedirs(self.dest_folder)

        while self.run_flag and self.index < sequence_length:
            source = self.source_files[self.index]
            shutil.copy2(source, self.dest_folder)
            self._mutex.lock()
            self.copy_one_file.emit(source)
            self._mutex.unlock()
            self.index += 1
        if self.index == sequence_length - 1:
            self.log.append('\n{} {}-{}'.format(utils.frame_to_pattern(self.source_files[0]),
                                                self.first,
                                                self.last))
        elif self.index > 0:
            self.log.append('\n{} {}-{}'.format(utils.frame_to_pattern(self.source_files[0]),
                                                self.first,
                                                self.first + self.index))
        self.finish.emit()


class FinishThread(QtCore.QThread):
    finish = QtCore.Signal()

    def __init__(self, view):
        super(FinishThread, self).__init__()
        self.run_flag = True
        self.view = view

    def run(self):
        while self.run_flag and len(self.view.thread_pool) > 1:
            continue
        self.finish.emit()