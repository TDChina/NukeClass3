from collections import OrderedDict
import re
import os


def get_shot_code(item_name):
    pattern = r'.*(?P<shot>\d{3}_\d{4}).*'
    match = re.match(pattern, item_name)
    if match:
        return match.groupdict().get('shot')
    return ''


def get_latest_versions(project, shot_code, step, file_format):
    results = []
    root = 'W:/projects/{}/publish/shots'.format(project.lower())
    for folder in os.listdir(root):
        if shot_code in folder and step in folder:
            folder_path = os.path.join(root, folder)
            if file_format == 'frame':
                results.append(os.path.join(folder_path, 'img', '{}.####.exr'.format(folder)))
            elif file_format == 'mov':
                result.append(os.path.join(folder_path, '{}.mov'.format(folder)))
    return results



def build_track_parse(trackitem_list, project, step, file_format):
    results = OrderedDict()
    for item in trackitem_list:
        shot_code = get_shot_code(item.name())
        versions = get_latest_versions(project,
                                       shot_code,
                                       step,
                                       file_format)
        if versions:
            results[shot_code] = versions
    return results


def get_track_name(bin_item_name):
    pattern = r'.*_(?P<task>[a-z0-9]+_[a-z0-9]+)$'
    result = re.match(pattern, bin_item_name)
    if result:
        return result.groupdict().get('task')
