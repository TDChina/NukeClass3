from batch_transcoder.backend.parsing.abstract_parser import AbstractParser

__parser_class_name__ = 'FrameRangeParser'


class FrameRangeParser(AbstractParser):

    def parse(self, source, current_data):
        dest_first = self._config_service.get_preset_config(
            'parsing/frame_range_parser/dest_first'
        )
        dest_last = int(current_data['last'] or source.sequence.end()) - int(current_data['first'] or source.sequence.start()) + dest_first
        current_data.update({
            'source_first': current_data['first'] or source.sequence.start(),
            'source_last': current_data['last'] or source.sequence.end(),
            'dest_first': str(dest_first),
            'dest_last': str(dest_last)
        })
        current_data.pop('first')
        current_data.pop('last')
        return current_data
