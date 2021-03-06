import os
import re

import nukescripts

pattern = r'[\/\w:]+\/(?P<show>\w+)_(?P<sequence>\w+)_(?P<shot>\w+)_(?P<step>\w+)_(?P<version>v\d{3})'

dailies_path_pattern = (
    'W:/projects/{show}/publish/shots/{sequence}/{shot}/{step}/{version}/mov/'
    '{show}_{sequence}_{shot}_{step}_{version}.mov')


def dailies_control(panel, read, slate, write):
	source = read['file'].value()
	match = re.match(pattern, source)
	if match:
		source_info = match.groupdict()
		write['file'].fromUserText(dailies_path_pattern.format(**source_info))
		write['create_directories'].setValue(True)
		slate['autoShow'].setValue(False)
		slate['autoVersion'].setValue(False)
		slate['showName'].setValue(source_info['show'].upper())
		slate['versionName'].setValue(os.path.splitext(os.path.basename(write['file'].value()))[0])
		slate['format'].setValue('HD_720')
		slate['headHandle'].setValue(5)
		slate['tailHandle'].setValue(5)
	else:
		write['disable'].setValue(True)
		panel.render_infos.pop(write.name())
