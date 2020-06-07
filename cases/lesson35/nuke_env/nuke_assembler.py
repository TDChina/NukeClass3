"""This module includes the NukeAssembler class."""

# Import built-in modules
from __future__ import print_function
import json
import os

# Import third-party modules
import nuke


class NukeAssembler(object):
    """This class provide basic functions to fill in node tree.

    Currently it will only fill in standard `source`, `render` and the Root
    nodes, so `source` and `render` nodes could remain default in the templates.
    This object has a `get` function to query parameter data by key path, so in
    other nodes we can automatically fill then by using python expression to get
    corresponding data from this object.

    """

    def __init__(self):
        """Initialize the NukeAssembler object and setup default nodes."""
        self.parameter_data = {}
        parameter_file = None

        template_path = nuke.root().name()
        if not template_path.endswith('.nk'):
            return

        # Parameter file will use same timestamp as template file.
        parameter_name = 'parameter_{}.json'.format(
            os.path.basename(template_path).split('.')[0].replace('template_',
                                                                  ''))

        parameter_path = os.path.join(os.path.dirname(template_path),
                                      parameter_name)

        print('parameter_file:', parameter_path)

        with open(parameter_path) as f:
            self.parameter_data = json.load(f)

        self.setup_source()
        self.setup_root()
        self.setup_slate()
        self.setup_render()
        
    def setup_source(self):
        """Setup source read node."""
        source = nuke.toNode('source')
        source['file'].fromUserText(
            '{} {}-{}'.format(self.data['source_path'],
                              self.data['source_first'],
                              self.data['source_last']))

    def setup_render(self):
        """Setup write node."""
        render = nuke.toNode('render')
        render['file'].fromUserText(self.data['dest_path'])

    def setup_root(self):
        """Setup Root node."""
        nuke.root()['first_frame'].setValue(self.data['dest_first'])
        nuke.root()['last_frame'].setValue(self.data['dest_last'])
        if 'fps' in self.data:
            nuke.root()['fps'].setValue(self.data['fps'])

    def setup_slate(self):
        slate = nuke.toNode('slate')
        if slate:
            slate['showName'].setValue(self.data['show'].upper())
            slate['versionName'].setValue('{show}_{sequence}_{shot}_{step}_{version}'.format(**self.data))

    @property
    def data(self):
        """Get the full parameter data."""
        return self.parameter_data

    def get(self, key_path):
        """Get data from the parameter data by specific key path.

        Args:
            key_path (str): Slash separated key path from the top to the
                specific key.

        Returns: Value of the parameter data.

        """
        config = self.data
        for k in key_path.split('/'):
            if config:
                config = config.get(k)
        if config or config == 0:
            return config
        return None
