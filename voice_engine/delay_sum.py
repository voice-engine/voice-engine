# -*- coding: utf-8 -*-

"""
Delay & Sum beamforming
"""

import numpy as np
import threading
try:
    import Queue as queue
except ImportError:
    import queue

from voice_engine.element import Element
from voice_engine.gcc_phat import gcc_phat


class DelaySum(Element):
    def __init__(self, channels=8, frames_size=160, max_offset=None):
        super(DelaySum, self).__init__()
        self.channels = channels
        self.frames_size = frames_size
        self.max_offset = max_offset
        self.sum = np.zeros(frames_size, dtype='int32')
        self.last = np.zeros(frames_size * self.channels, dtype='int16')

        self.queue = queue.Queue()
        self.done = False

    def put(self, data):
        self.queue.put(data)

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.done = True

    def run(self):
        self.done = False
        while not self.done:
            data = self.queue.get()
            data = np.fromstring(data, dtype='int16')
            offsets = [0] * self.channels
            for i in range(1, self.channels):
                offsets[i], _ = gcc_phat(data[i::self.channels], data[0::self.channels], max_tau=self.max_offset,
                                         interp=1)

            self.sum.fill(0)
            half = int(self.frames_size / 2)
            for i in range(self.channels):
                offset = int(offsets[i])
                self.sum[:half - offset] += (self.last[i::self.channels])[half + offset:]
                self.sum[half - offset:] += (data[i::self.channels])[:half + offset]

            self.last = data

            out = np.array(self.sum / self.channels, dtype='int16')
            super(DelaySum, self).put(out.tostring())
