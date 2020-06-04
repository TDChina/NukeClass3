import os

from build_track.mvc.constants import TABLE_HEADER, STEPS
from build_track.hiero_utils import (get_selected_video_trackitems, 
                                     prepare_build_items, 
                                     BuildTrackProcess)
from build_track.utils import get_shot_code, build_track_parse


class BuildTrackController(object):
    def __init__(self, view):
        self.view = view
        self.selection = get_selected_video_trackitems()
        if self.selection:
            self.project = self.selection[0].parent().parent().project()
            self.project_name = self.project.name()
            self.init_data()
        self.result_versions = []
        self.connect_slots()

    def connect_slots(self):
        self.view.find_button.clicked.connect(self.find_versions)
        self.view.build_button.clicked.connect(self.build)
        self.view.cancel_button.clicked.connect(self.view.close)

    def show_ui(self):
        self.view.show()

    def init_data(self):
        if self.project_name:
            self.view.project_text.setText(self.project_name)
        for step in STEPS:
            self.view.step_combobox.addItem(step)
        for _format in ('frame', 'mov'):
            self.view.format_combobox.addItem(_format)

        shots = []
        for item in self.selection:
            shots.append({TABLE_HEADER[0]['attr']: item.name()})
        self.view.result_table.model.setDataList(shots)
        self.view.result_table.resizeHeader()

    def find_versions(self):
        project = self.view.project_text.text()
        step = self.view.step_combobox.currentText()
        _format = self.view.format_combobox.currentText()

        self.result_versions = build_track_parse(self.selection,
                                                       project,
                                                       step,
                                                       _format)
        self.set_result_table(self.result_versions)

    def set_result_table(self, result_versions):
        data_list = []
        for shot in result_versions:
            version_count = 0
            for version in result_versions[shot]:
                version_code = (os.path.basename(version)).split('.')[0]
                data_list.append({TABLE_HEADER[0]['attr']:
                                  shot if version_count == 0 else '',
                                  TABLE_HEADER[1]['attr']:
                                  version_code})
                version_count += 1
        self.view.result_table.model.setDataList(data_list)
        self.view.result_table.resizeHeader()

    def prepare_build_dict(self):
        build_dict = {}
        for row in self.view.result_table.selectionModel().selectedRows():
            version_name = str(row.child(row.row(), 1).data())
            shot_code = get_shot_code(version_name)

            trackitems = [i for i in self.selection if shot_code in i.name()]
            trackitem = trackitems[0]
            selected_version = [version for version in
                                self.result_versions[shot_code]
                                if (os.path.basename(version)).split('.')[0] == version_name][0]
            if trackitem in build_dict:
                build_dict[trackitem][1].append(selected_version)
            else:
                build_dict[trackitem] = (trackitems,
                                         [selected_version])
        return build_dict

    def build(self):
        if not self.view.result_table.selectionModel().selectedRows():
            QtWidgets.QMessageBox.critical(self,
                                           'Warning',
                                           'You haven\'t select any version.')
            return
        build_dict = self.prepare_build_dict()
        import_list = prepare_build_items(self.project,
                                          build_dict)
        build_track = BuildTrackProcess(self.project_name)
        build_track.buildtrack_process(self.project, import_list)
