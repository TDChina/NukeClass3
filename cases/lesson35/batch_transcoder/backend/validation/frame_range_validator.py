from batch_transcoder.backend.validation.abstract_validator import AbstractValidator

__validator_class_name__ = 'FrameRangeValidator'


class HandleLengthError(Exception):
    pass


class DurationError(Exception):
    pass


class MissingFrameError(Exception):
    pass


class FrameRangeValidator(AbstractValidator):

    def validate(self, source):
        exceptions = []

        # validate missing frames
        if source.sequence.missing() and not \
                self._config_service.get_preset_config(
                    'validation/frame_range_validator/allow_missing_frames'):
            missing = ', '.join([str(f) for f in source.sequence.missing()])
            exceptions.append(MissingFrameError(
                'Missing frames {} in source.'.format(missing)))

        # validate handle length
        head = int(source.data.get('head'))
        tail = int(source.data.get('tail'))
        if head + tail >= (source.sequence.length()):
            exceptions.append(
                HandleLengthError('No content frames besides handles.'))

        # validate duration
        source_length = source.sequence.length()
        dest_length = int(source.data.get(
            'dest_last')) - int(source.data.get('dest_first')) + 1
        if not self._config_service.get_preset_config(
                'validation/source/frame_range_validator/allow_retime'):
            if dest_length > source_length:
                exceptions.append(
                    DurationError(
                        'Source duration does not match destination duration.'))

        return exceptions
