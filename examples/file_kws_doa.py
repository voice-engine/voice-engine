"""
Read audio from a file, and then search the keyword "snowboy".
After finding the keyword, Direction Of Arrival (DOA) is estimated.
"""

import sys
import time
from voice_engine.file_source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.doa_respeaker_6p1_mic_array import DOA


def main():
    if len(sys.argv) < 2:
        print('Usage: {} audio.wav')
        sys.exit(1)

    src = Source(sys.argv[1])
    ch0 = ChannelPicker(channels=src.channels, pick=0)
    kws = KWS()
    doa = DOA(rate=16000)

    src.link(ch0)
    ch0.link(kws)
    src.link(doa)

    def on_detected(keyword):
        print('detected {} at direction {}'.format(keyword, doa.get_direction()))

    kws.set_callback(on_detected)

    src.recursive_start()
    while src.is_active():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()

    # wait a second to allow other threads to exit
    time.sleep(1)


if __name__ == '__main__':
    main()
