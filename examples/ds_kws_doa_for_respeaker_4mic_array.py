"""
Record audio from a 4 mic array, and then search the keyword "snowboy".
After finding the keyword, Direction Of Arrival (DOA) is estimated.

The hardware is respeaker 4 mic array for raspberry pi:
    https://www.seeedstudio.com/ReSpeaker-Mic-Array-Far-field-w--7-PDM-Microphones--p-2719.html
"""

import time
from voice_engine.source import Source
from voice_engine.kws import KWS
from voice_engine.doa_respeaker_4mic_array import DOA
from voice_engine.delay_sum import DelaySum
from pixel_ring import pixel_ring
from pixel_ring.echo import Pattern
from gpiozero import LED

pixel_ring.change_pattern(Pattern)
power = LED(5)
power.on()

max_offset = int(16000 * 0.081 / 340)


def main():
    src = Source(rate=16000, frames_size=320, channels=4)
    ds = DelaySum(channels=4, frames_size=src.frames_size, max_offset=max_offset)
    kws = KWS()
    doa = DOA(rate=16000, chunks=20)

    src.link(ds)
    ds.link(kws)

    src.link(doa)

    def on_detected(keyword):
        direction = doa.get_direction()
        pixel_ring.wakeup(direction)
        print('detected {} at direction {}'.format(keyword, direction))

    kws.on_detected = on_detected

    src.recursive_start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('quit')
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()
