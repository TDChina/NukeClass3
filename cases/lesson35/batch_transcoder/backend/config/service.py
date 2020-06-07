import os

from batch_transcoder.backend.config.config import Config
from batch_transcoder.backend.utils import constants


class ConfigService(object):

    def __init__(self, show=None, preset=None):
        self.global_config = Config('global')
        self._show = show
        self._preset = preset

    def get_global_config(self, key_path):
        return self.global_config.get(key_path)

    def get_preset_config(self, key_path):
        config = Config(self._show, self._preset)
        return config.get(key_path)

    def update_context(self, show, preset):
        self._show = show
        self._preset = preset

    @staticmethod
    def get_show_list():
        return [s.upper() for s in os.listdir('{}/show'.format(constants.CONFIG_ROOT))]

    @staticmethod
    def get_preset_list(show):
        return [os.path.splitext(p)[0] for p in os.listdir('{}/show/{}'.format(constants.CONFIG_ROOT, show))]
