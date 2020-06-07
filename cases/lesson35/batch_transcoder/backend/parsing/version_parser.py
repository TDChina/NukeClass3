from batch_transcoder.backend.parsing.abstract_parser import AbstractParser

__parser_class_name__ = 'VersionParser'


class VersionParser(AbstractParser):

    def parse(self, source, current_result):
        custom_version = self._config_service.get_preset_config(
            'parsing/version_parser/custom_version')
        if custom_version:
            current_result['version'] = custom_version
        elif 'version' not in current_result:
            current_result['version'] = 'v001'
        return current_result
