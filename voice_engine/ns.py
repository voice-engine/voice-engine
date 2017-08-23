# -*- coding: utf-8 -*-

"""
Noise Suppression (NS) from webrtc audio processing
"""

from webrtc_audio_processing import AP

from .element import Element


class NS(Element):
    def __init__(self, rate=16000, channels=1):
        super(NS, self).__init__()

        self.ap = AP(enable_ns=True)
        self.ap.set_stream_format(rate, channels)

    def put(self, data):
        data = self.ap.process_stream(data)

        super(NS, self).put(data)



