import os


class TemplateConfigError(Exception):
    pass


class TemplateService(object):

    def __init__(self, config_service):
        self._config_service = config_service

    def _get_temlate_folder(self):
        path = self._config_service.get_preset_config(
            'transcoding/template/path')
        name = self._config_service.get_preset_config(
            'transcoding/template/name'
        )
        return os.path.join(path, name)

    def get_template_file(self):
        folder = self._get_temlate_folder()
        template_file = os.path.join(folder, 'template.nk')
        if not os.path.isfile(template_file):
            raise TemplateConfigError('can not find corresponding template file.')
        return template_file

    def get_parameter_file(self):
        folder = self._get_temlate_folder()
        parameter_file = os.path.join(folder, 'parameters.yaml')
        if not os.path.isfile(parameter_file):
            return None
        return parameter_file
