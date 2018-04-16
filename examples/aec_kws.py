"""
ReSpeaker V2 and ReSpeaker 6 Mic Array for Raspberry Pi 
have 8 input channels with 6 microphones and 2 channels' playback-loopback.
In this application, we use 1 channel microphone data and 1 channel playback-loopback data
to do AEC (Acoustic Echo Cancellation). The algorithm is from Speex.

Requirement:
    pip install speexdsp
"""

import sys
import time
from voice_engine.source import Source
from voice_engine.ec import EC
from voice_engine.kws import KWS

count = 0


def main():
    src = Source(rate=16000, channels=8, frames_size=1600)
    ec = EC(channels=src.channels, capture=0, playback=6)
    kws = KWS(sensitivity=0.7)

    def on_detected(keyword):
        global count
        count += 1
        print('detected {}'.format(keyword))

    kws.on_detected = on_detected

    src.pipeline(ec, kws)

    src.pipeline_start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    print('total = {}'.format(count))
    src.pipeline_stop()


if __name__ == '__main__':
    main()
