

# -*- coding: utf-8 -*-

"""
Save audio to file
"""

import wave
from .element import Element


class FileSink(Element):
    def __init__(self, name, rate=16000, channels=1, width=2):
        super(FileSink, self).__init__()
        self.file_name = name
        self.rate = rate
        self.channels = channels
        self.width = width

        self._wav = None

    def put(self, data):
        self._wav.writeframes(data)

    def start(self):
        self._wav = wave.open(self.file_name, 'w')
        self._wav.setframerate(self.rate)
        self._wav.setnchannels(self.channels)
        self._wav.setsampwidth(self.width)

    def stop(self):
        self._wav.close()
