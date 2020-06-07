from importlib import import_module

from batch_transcoder.backend.utils.context_manager import get_module


class ParsingService(object):

    def __init__(self, config_service):
        self.config_service = config_service

    def get_parsers(self):
        parser_names = self.config_service.get_preset_config(
            'parsing/parsers')
        parsers = []
        custom_path = self.config_service.get_preset_config(
            'parsing/custom_loading_path')
        for name in parser_names:
            if custom_path:
                try:
                    module = get_module(name, custom_path)
                except ImportError:
                    module = import_module(
                        'batch_transcoder.backend.parsing.{}'.format(name))
            else:
                module = import_module(
                    'batch_transcoder.backend.parsing.{}'.format(name))
            cls = getattr(module, module.__parser_class_name__)
            parser = cls(self.config_service)
            parsers.append(parser)
        return parsers
