# -*- coding: utf-8 -*- 
#
# dB(A) A-weighting
#
# Requirements:
#   pip install git+https://github.com/endolith/waveform_analysis.git@master

import numpy as np
from waveform_analysis.weighting_filters import A_weight

from voice_engine.element import Element


class DBA(Element):
    def __init__(self, rate, channels, bits_per_sample=16):
        super(DBA, self).__init__()
        self.rate = rate
        self.channels = channels
        if bits_per_sample == 32:
            self.type = 'int32'
            self.width = 4
            self.top = 20 * np.log10(2 ** 31 - 1)
        else:
            self.type = 'int16'
            self.width = 2
            self.top = 20 * np.log10(2 ** 15 - 1)

    def put(self, data):
        buf = np.fromstring(data, dtype=self.type)
        v = [[], []]
        for ch in range(self.channels):
            mono = buf[ch::self.channels]
            # dbfs = 20 * np.log10(np.sqrt(np.mean(np.square(mono, dtype='float')))) - self.top
            dbfs = 10 * np.log10(np.mean(np.square(mono, dtype='float'))) - self.top
            v[0].append(int(dbfs))

            w = A_weight(mono, self.rate)

            # dba = 20 * np.log10(np.sqrt(np.mean(w**2))) - self.top
            dba = 10 * np.log10(np.mean(w ** 2)) - self.top
            v[1].append(int(dba))

        super(DBA, self).put(data)
        print('dBFS {}, dB(A) {}'.format(v[0], v[1]))


def main():
    import time
    from voice_engine.source import Source

    src = Source(rate=48000, channels=2, frames_size=4800)
    dba = DBA(rate=src.rate, channels=src.channels)

    src.pipeline(dba)

    src.pipeline_start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.pipeline_stop()


if __name__ == '__main__':
    main()
