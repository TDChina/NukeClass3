import os




FILE_EXTENSIONS = (
    '.cin',
    '.dpx',
    '.exr',
    '.gif',
    '.jpeg',
    '.jpg',
    '.png',
    '.tga',
    '.tif',
    '.tiff'
)


class MultipleSequenceError(Exception):
    pass


class NoSourceFoundError(Exception):
    pass


class Source(object):

    def __init__(self, root, sequence):
        self.root = root
        self.sequence = sequence
        self.data = {}

    @property
    def name(self):
        return os.path.basename(self.sequence.path())

