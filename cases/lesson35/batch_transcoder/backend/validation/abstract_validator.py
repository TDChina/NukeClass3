import abc


class AbstractValidator(object):

    def __init__(self, config_service):
        self._config_service = config_service

    @abc.abstractmethod
    def validate(self, source):
        pass
