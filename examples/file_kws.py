"""
Read audio from a file, and then search the keyword "snowboy".
"""

import sys
import time
from voice_engine.file_source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.ns import NS
from voice_engine.kws import KWS


def main():
    if len(sys.argv) < 2:
        print('Usage: {} audio.wav')
        sys.exit(1)

    src = Source(sys.argv[1])
    ch0 = ChannelPicker(channels=src.channels, pick=0)
    ns = NS(rate=src.rate, channels=1)
    kws = KWS()

    src.pipeline(ch0, kws)
    # src.pipeline(ch0, ns, kws)

    def on_detected(keyword):
        print('detected {}'.format(keyword))

    kws.set_callback(on_detected)

    src.pipeline_start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.pipeline_stop()

    # wait a second to allow other threads to exit
    time.sleep(1)


if __name__ == '__main__':
    main()
