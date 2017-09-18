# -*- coding: utf-8 -*-

"""
WebRTC Voice Activity Detector (VAD)
"""

import sys
from webrtcvad import Vad
from .element import Element


class VAD(Element):
    def __init__(self, rate=16000, mode=0):
        super(VAD, self).__init__()

        self.rate = rate
        self.vad = Vad(mode)

    def put(self, data):
        voice = '1' if self.vad.is_speech(data, self.rate) else '0'
        sys.stdout.write(voice)
        sys.stdout.flush()

        super(VAD, self).put(data)
