# -*- coding: utf-8 -*-

"""
Select channel 0 from multiple channels
"""

import numpy as np

from .element import Element


class ChannelPicker(Element):
    def __init__(self, channels=8, pick=0, bits_per_sample=16):
        super(ChannelPicker, self).__init__()
        self.channels = channels
        self.pick = pick
        if bits_per_sample == 16:
            self.dtype = np.int16
        elif bits_per_sample == 32:
            self.dtype = np.int32
        else:
            raise ValueError

    def put(self, data):
        data = np.fromstring(data, dtype=self.dtype)
        data = data[self.pick::self.channels].tostring()
        super(ChannelPicker, self).put(data)
