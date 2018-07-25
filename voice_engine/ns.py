# -*- coding: utf-8 -*-

"""
Noise Suppression (NS) from webrtc audio processing
"""

from webrtc_audio_processing import AP

from .element import Element


class NS(Element):
    def __init__(self, rate=16000, channels=1):
        super(NS, self).__init__()

        self.rate = rate
        self.channels = channels
        self._buf = b''
        self._bytes_10ms = int(rate * channels * 2 / 100)

        self.ap = AP(enable_ns=True)
        self.ap.set_stream_format(rate, channels)

    def put(self, data):
        self._buf += data
        while len(self._buf) >= self._bytes_10ms:
            data = self._buf[:self._bytes_10ms]
            self._buf = self._buf[self._bytes_10ms:]

            # webrtc audio processing only support processing 10 ms audio each time
            data = self.ap.process_stream(data)

            super(NS, self).put(data)
