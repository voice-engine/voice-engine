# -*- coding: utf-8 -*-

"""
WebRTC Voice Activity Detector (VAD)
"""

from webrtcvad import Vad

from .element import Element


class VAD(Element):
    def __init__(self, rate=16000, mode=0, duration=1000, on_inactive=None):
        super(VAD, self).__init__()

        self.rate = rate
        self.vad = Vad(mode)
        self.on_inactive = on_inactive
        self.limit_inactive_cnt = duration / 10  # a frame is 10 ms
        self.current_inactive_cnt = 0

    def put(self, data):
        active = self.vad.is_speech(data, self.rate)
        if active:
            self.current_inactive_cnt = 0
        else:
            self.current_inactive_cnt += 1

        if self.current_inactive_cnt == self.limit_inactive_cnt:
            if callable(self.on_inactive):
                self.on_inactive()
            self.current_inactive_cnt = 0
        super(VAD, self).put(data)

    def on_inactive(self, cb):
        self.on_inactive = cb
