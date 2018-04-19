# -*- coding: utf-8 -*-

import audioop
import numpy as np
from voice_engine.element import Element


class DBFS(Element):
    def __init__(self, channels=1, bits_per_sample=16):
        super(DBFS, self).__init__()
        self.channels = channels
        if bits_per_sample == 32:
            self.type = 'int32'
            self.width = 4
            self.top = 20 * np.log10(2**31 - 1)
        else:
            self.type = 'int16'
            self.width = 2
            self.top = 20 * np.log10(2**15 - 1)

    def put(self, data):
        buf = np.fromstring(data, dtype=self.type)
        dbfs = []
        for ch in range(self.channels):
            mono = buf[ch::self.channels].tostring()
            rms = 20 * np.log10(audioop.rms(mono, self.width)) - self.top
            dbfs.append(int(rms))

        super(DBFS, self).put(data)
        print(dbfs)


def main():
    import time
    from voice_engine.source import Source

    src = Source(rate=16000, channels=2, frames_size=1600)
    dbfs = DBFS(channels=src.channels)


    src.pipeline(dbfs)

    src.pipeline_start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.pipeline_stop()


if __name__ == '__main__':
    main()