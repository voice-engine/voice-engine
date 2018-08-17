# -*- coding: utf-8 -*-

"""
Keyword spotting using snowboy
"""

import os
import sys
import threading
import wave

if sys.version_info[0] < 3:
    import Queue as queue
else:
    import queue

from .element import Element


class FileSink(Element):
    def __init__(self, name, rate=16000, channels=1, width=2):
        super(FileSink, self).__init__()
        self.file_name = name
        self.rate = rate
        self.channels = channels
        self.width = width

        self._wav = None

        self.queue = queue.Queue()
        self.done = False
        self.thread = None


    def put(self, data):
        self.queue.put(data)

    def start(self):
        self._wav = wave.open(self.file_name, 'w')
        self._wav.setframerate(self.rate)
        self._wav.setnchannels(self.channels)
        self._wav.setsampwidth(self.width)

        self.done = False
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.done = True
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=3)

    def run(self):
        while not self.done:
            try:
                data = self.queue.get(timeout=1)
            except queue.Empty:
                break

            self._wav.writeframes(data)

        self._wav.close()



