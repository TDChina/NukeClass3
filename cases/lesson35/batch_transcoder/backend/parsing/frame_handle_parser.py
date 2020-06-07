from batch_transcoder.backend.parsing.abstract_parser import AbstractParser

__parser_class_name__ = 'FrameHandleParser'


class FrameHandleParser(AbstractParser):

    def parse(self, source, current_result):
        handle_config = self._config_service.get_preset_config(
            'parsing/frame_handle_parser')
        head = handle_config.get('head_handle', 0)
        tail = handle_config.get('tail_handle', 0)

        current_result.update({'head': str(head), 'tail': str(tail)})
        return current_result
