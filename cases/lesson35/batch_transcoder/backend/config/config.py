# coding=utf-8

from copy import deepcopy
import yaml

from batch_transcoder.backend.utils.constants import CONFIG_ROOT


class ConfigMissingError(Exception):
    pass


def merge_dict(source_dict, dest_dict):
    for key in source_dict:
        if key in dest_dict and isinstance(source_dict[key], dict) and \
                isinstance(dest_dict[key], dict):
            merge_dict(source_dict[key], dest_dict[key])
        else:
            dest_dict[key] = deepcopy(source_dict[key])


def get_config(source_config, key_path):
    config = source_config
    for k in key_path.split('/'):
        if config:
            config = config.get(k)
    if config:
        return config
    return None


class Config(object):

    def __init__(self, context, preset=None):
        if context != 'global' and not preset:
            raise TypeError('You should specify a preset name.')
        self.context = context
        self.preset = preset
        self.config_data = self._get_config_data()

    def _get_config_data(self):
        global_config_file = '{}/global.yaml'.format(CONFIG_ROOT)

        with open(global_config_file) as f:
            global_config_data = yaml.safe_load(f)

        if self.context == 'global':
            return global_config_data
        preset_config_file = '{}/show/{}/{}.yaml'.format(CONFIG_ROOT, self.context, self.preset)
        with open(preset_config_file) as f:
            preset_config_data = yaml.safe_load(f)
        if not preset_config_data:
            preset_config_data = {}
        merge_dict(preset_config_data, global_config_data)
        return global_config_data

    def get(self, key_path):
        return get_config(self.config_data, key_path)
