import abc


class AbstractParser(object):

    def __init__(self, config_service):
        self._config_service = config_service

    @abc.abstractmethod
    def parse(self, source, current_result):
        pass
