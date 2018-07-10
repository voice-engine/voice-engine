# -*- coding: utf-8 -*-
"""Audio source that reads raw audio file"""

import logging
import threading

from .element import Element

logger = logging.getLogger(__file__)


class Source(Element):
    def __init__(self, name, rate=16000, channels=1, frame_size=160):
        super(Source, self).__init__()

        self.name = name
        self.rate = rate
        self.channels = channels
        self.frame_size = frame_size
        self.done = False

    def run(self):
        with open(self.name, 'rb') as f:
            size = self.channels * self.frame_size * 2
            while not self.done:
                frames = f.read(size)
                if not frames:
                    self.done = True
                    break
                elif len(frames) != size:
                    frames = frames.rjust(size)

                super(Source, self).put(frames)

    def start(self):
        self.done = False

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.done = True

    def is_active(self):
        return not self.done
