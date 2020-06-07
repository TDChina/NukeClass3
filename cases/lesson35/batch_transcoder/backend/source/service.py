import os

import pyseq

from batch_transcoder.backend.source.source import Source


class SourceService(object):

    def __init__(self, config_service):
        self._config_service = config_service

    def _get_allowed_files(self, files):
        allowed_extensions = tuple(self._config_service.get_preset_config(
            'validation/drag_in/extensions'))
        files = [
            f for f in files if f.endswith(allowed_extensions)
            and not f.startswith('.')
        ]
        return files

    def add_source(self, path):
        if os.path.isfile(path):
            _file = self._get_allowed_files([path])
            if not _file:
                return []
            return [Source(os.path.dirname(path),
                           pyseq.get_sequences(_file[0])[0])]
        elif os.path.isdir(path):
            result = []
            for root, _, files in os.walk(path):
                allowed_files = self._get_allowed_files(files)
                sequences = pyseq.get_sequences(allowed_files)
                sources = []
                for sequence in sequences:
                    sources.append(Source(root, sequence))
                result.extend(sources)
            return result
        return []

    def clear_sources(self):
        pass


