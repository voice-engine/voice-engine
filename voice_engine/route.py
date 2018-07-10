# -*- coding: utf-8 -*-


import numpy as np

from .element import Element


class Route(Element):
    def __init__(self, channels=2):
        super(Route, self).__init__()
        self.channels = channels
        self.sinks = [None] * self.channels

    def link(self, sinks):
        for i, sink in enumerate(sinks):
            self.sinks[i] = sink

    def put(self, data):
        data = np.fromstring(data, dtype='int16')
        for ch in range(self.channels):
            mono = data[ch::self.channels].astype('int16').tostring()
            if self.sinks[ch]:
                self.sinks[ch].put(mono)


def main():
    import time
    from voice_engine.source import Source
    from voice_engine.kws import KWS

    src = Source(rate=16000, channels=2, frames_size=1600)
    route = Route(channels=src.channels)
    kws = []

    def gen(channel):
        def on_detected(keyword):
            print('detected at channel {}'.format(channel))

        return on_detected

    for ch in range(src.channels):
        k = KWS(sensitivity=0.5)
        k.set_callback(gen(ch))
        kws.append(k)

    src.pipeline(route, kws)

    src.pipeline_start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.pipeline_stop()


if __name__ == '__main__':
    main()
