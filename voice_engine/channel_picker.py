# -*- coding: utf-8 -*-

"""
Select channel 0 from multiple channels
"""

import numpy as np
from .element import Element


class ChannelPicker(Element):
    def __init__(self, channels=8, pick=0):
        super(ChannelPicker, self).__init__()
        self.channels = channels
        self.pick = pick

    def put(self, data):
        data = np.fromstring(data, dtype='int16')
        data = data[self.pick::self.channels].tostring()
        super(ChannelPicker, self).put(data)

