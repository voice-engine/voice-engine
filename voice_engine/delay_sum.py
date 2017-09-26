# -*- coding: utf-8 -*-

"""
Delay & Sum beamforming
"""

import numpy as np
from voice_engine.element import Element
from voice_engine.gcc_phat import gcc_phat


class DelaySum(Element):
    def __init__(self, channels=8, frames_size=160, max_delay=None):
        super(DelaySum, self).__init__()
        self.channels = channels
        self.frames_size = frames_size
        self.max_delay = max_delay
        self.sum = np.zeros(frames_size, dtype='int32')
        self.last = np.zeros(frames_size * self.channels, dtype='int16')

    def put(self, data):
        data = np.fromstring(data, dtype='int16')
        offsets = [0] * self.channels
        for i in range(1, self.channels):
            offsets[i], _ = gcc_phat(data[i::self.channels], data[0::self.channels], max_tau=self.max_delay, interp=1)

        self.sum.fill(0)
        half = int(self.frames_size / 2)
        for i in range(self.channels):
            offset = int(offsets[i])
            self.sum[:half-offset] += (self.last[i::self.channels])[half+offset:]
            self.sum[half-offset:] += (data[i::self.channels])[:half+offset]

        self.last = data

        out = np.array(self.sum / (self.channels - 1), dtype='int16')
        super(DelaySum, self).put(out.tostring())

