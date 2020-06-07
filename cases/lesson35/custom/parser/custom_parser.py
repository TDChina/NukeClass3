from batch_transcoder.backend.parsing.abstract_parser import AbstractParser

__parser_class_name__ = 'CustomParser'



class CustomParser(AbstractParser):

    def parse(self, source, current_result):
        current_result.update({'custom1': 'aaa', 'custom2': 'bbb', 'first': '996'})
        return current_result
