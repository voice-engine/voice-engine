# -*- coding: utf-8 -*-

"""
EC (Echo Canceller)

Playback is captured at one of mic array channels
"""
import sys

if sys.version_info[0] < 3:
    import Queue as queue
else:
    import queue

import threading
import numpy as np
from speexdsp import EchoCanceller

from .element import Element


class EC(Element):
    def __init__(self, rate=16000, channels=8, capture=1, playback=6, frames_size=256, filter_length=2048):
        super(EC, self).__init__()
        self.channels = channels
        self.rec_channel = capture
        self.far_channel = playback
        self.frames_size = frames_size
        self.echo_canceller = EchoCanceller.create(frames_size, filter_length, rate, 1, 1)
        self.queue = queue.Queue()
        self.done = False
        self.bypass = False

    def put(self, data):
        self.queue.put(data)

    def start(self):
        self.done = False
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.done = True

    def run(self):
        data = ''
        frames_bytes = self.frames_size * self.channels * 2
        while not self.done:
            data += self.queue.get()
            while len(data) >= frames_bytes:
                buf = np.fromstring(data[:frames_bytes], dtype='int16')
                rec = buf[self.rec_channel::self.channels].tostring()
                if not self.bypass:
                    far = buf[self.far_channel::self.channels].tostring()
                    out = self.echo_canceller.process(rec, far)
                else:
                    out = rec

                super(EC, self).put(out)

                data = data[frames_bytes:]


def main():
    import time
    from voice_engine.source import Source

    src = Source(rate=16000, channels=2, frames_size=1600)
    ec = EC(channels=src.channels, capture=0, playback=1)

    src.pipeline(ec)
    src.pipeline_start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.pipeline_stop()


if __name__ == '__main__':
    main()
