from batch_transcoder.backend.utils.regex_processor import get_regex_keys

from batch_transcoder.backend.parsing.abstract_parser import AbstractParser

__parser_class_name__ = 'DestPathParser'


class SourceDurationError(Exception):
    pass


class DestPathParser(AbstractParser):

    def parse(self, source, current_result):
        dest_pattern = self._config_service.get_preset_config('transcoding/dest_pattern')
        for key in get_regex_keys(dest_pattern, wildcard=True):
            if key not in current_result:
                current_result[key] = ''
        return current_result
