# -*- coding: utf-8 -*-

"""
Save audio to file
"""

from .element import Element


class FileSink(Element):
    def __init__(self, name):
        super(FileSink, self).__init__()
        self.file_name = name
        self.f = None

    def put(self, data):
        self.f.write(data)

    def start(self):
        self.f = open(self.file_name, 'w')

    def stop(self):
        self.f.close()
