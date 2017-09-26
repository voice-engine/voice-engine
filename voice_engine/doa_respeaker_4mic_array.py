# -*- coding: utf-8 -*-

"""
Time Difference of Arrival for ReSpeaker 4 Mic Array
"""

import numpy as np
import collections
from .gcc_phat import gcc_phat
from .element import Element


SOUND_SPEED = 340.0

MIC_DISTANCE_4 = 0.081
MAX_TDOA_4 = MIC_DISTANCE_4 / float(SOUND_SPEED)


class DOA(Element):
    def __init__(self, rate=16000, chunks=10):
        super(DOA, self).__init__()

        self.queue = collections.deque(maxlen=chunks)
        self.sample_rate = rate

        self.pair = [[0, 2], [1, 3]]

    def put(self, data):
        self.queue.append(data)

        super(DOA, self).put(data)

    def get_direction(self):
        tau = [0, 0]
        theta = [0, 0]

        buf = b''.join(self.queue)
        buf = np.fromstring(buf, dtype='int16')
        for i, v in enumerate(self.pair):
            tau[i], _ = gcc_phat(buf[v[0]::4], buf[v[1]::4], fs=self.sample_rate, max_tau=MAX_TDOA_4, interp=1)
            theta[i] = np.arcsin(tau[i] / MAX_TDOA_4) * 180 / np.pi

        if np.abs(theta[0]) < np.abs(theta[1]):
            if theta[1] > 0:
                best_guess = (theta[0] + 360) % 360
            else:
                best_guess = (180 - theta[0])
        else:
            if theta[0] < 0:
                best_guess = (theta[1] + 360) % 360
            else:
                best_guess = (180 - theta[1])

            best_guess = (best_guess + 270) % 360

        best_guess = (-best_guess + 120) % 360

        return best_guess
