"""This module will be added into NUKE_PATH and loaded when launching Nuke."""

# Import built-in modules
# We need to import this module so that we can use this module with python
# expression in nuke script.
import time

# Import local modules
# We need to import this module because in the onScriptLoad callback of the
# template nuke script it will instantiate this class.

from nuke_assembler import NukeAssembler
from slate_knob_changed import *


class Dummy(object):
    """A dummy class acting as the NukeAssembler class."""

    def __init__(self, *args, **kwargs):
        """Initialize the dummy object.

        This object will do nothing, only provide dummy interfaces that are
        needed during the creation of the node tree.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(Dummy, self).__init__(*args, **kwargs)

    def get(self, key_path):
        """Dummy interface of the `get` function of NukeAssembler object.

        Args:
            key_path (str): A key path to query values from.

        Returns (str): A blank string.

        """
        return ''


# We need this dummy instance because Nuke will create nodes and evaluate all
# expressions into them before call the onScriptLoad callback, using this dummy
# object will bypass NameError and AttributeError.
assembler = Dummy()
