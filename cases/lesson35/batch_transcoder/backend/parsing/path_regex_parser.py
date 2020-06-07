import re

from batch_transcoder.backend.utils.regex_processor import get_regex_keys
from batch_transcoder.backend.parsing.abstract_parser import AbstractParser

__parser_class_name__ = 'PathRegexParser'


class RegexParseError(Exception):
    pass


class PathRegexParser(AbstractParser):

    def parse(self, source, current_result):
        config = self._config_service.get_preset_config(
            'parsing/path_regex_parser')
        path_regex = config.get('path_regex')
        basename_regex = config.get('basename_regex')
        path = source.sequence.path()
        for regex in (path_regex, basename_regex):
            if not regex:
                continue
            match = re.search(regex, path)
            if not match:
                for key in get_regex_keys(regex):
                    current_result[key] = ''
                continue
            match_dict = match.groupdict()
            for key in match_dict:
                current_result[key] = match_dict[key]
        return current_result
