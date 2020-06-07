from importlib import import_module


class ValidationService(object):
    
    def __init__(self, config_service):
        self.config_service = config_service

    def get_drag_in_validators(self):
        validator_names = self.config_service.get_preset_config(
            'validation/drag_in/validators')
        return self._get_validator_classes(validator_names)

    def get_source_validators(self):
        validator_names = self.config_service.get_preset_config(
            'validation/source/validators')
        return self._get_validator_classes(validator_names)

    def _get_validator_classes(self, validator_names):
        if not validator_names:
            return []
        validators = []
        for name in validator_names:
            module = import_module(
                'batch_transcoder.backend.validation.{}'.format(name))
            cls = getattr(module, module.__validator_class_name__)
            validator = cls(self.config_service)
            validators.append(validator)
        return validators
