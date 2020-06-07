from batch_transcoder.backend.validation.abstract_validator import AbstractValidator

__validator_class_name__ = 'SourceInfoValidator'


class MissingInfoError(Exception):
    pass


class SourceInfoValidator(AbstractValidator):

    def validate(self, source):
        exceptions = []
        for key in source.data:
            if not source.data[key]:
                exceptions.append(
                    MissingInfoError('No {} value in source info.'.format(key)))
                break
        return exceptions
