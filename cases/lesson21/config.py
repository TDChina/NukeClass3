path_pattern = r'[\/\w:]+\/(?P<show>\w+)_(?P<sequence>sc\d+)_(?P<shot>sh\d+)_(?P<step>\w+)_(?P<version>v\d{3})'

task_names = {
    'comp': ['matte', 'slap', 'precomp', 'paint', 'final'],
    'lgt': ['precomp', 'final']
}

write_path_pattern = (
    'W:/projects/{show}/publish/shots/{sequence}/{shot}/{step}/{task}/{version}/'
    '{show}_{sequence}_{shot}_{step}-{task}_{version}.{format}')