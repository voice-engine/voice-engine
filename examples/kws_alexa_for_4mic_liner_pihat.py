

import time
from voice_engine.source import Source
from voice_engine.kws import KWS
from voice_engine.channel_picker import ChannelPicker
# from voice_engine.doa_respeaker_v2_6mic_array import DOA
# from voice_engine.delay_sum import DelaySum
from avs.alexa import Alexa



max_offset = int(16000 * 0.081 / 340)


def main():
    src = Source(rate=16000, frames_size=320, channels=8)
    # ds = DelaySum(channels=8, frames_size=src.frames_size, max_offset=max_offset)
    ch0 = ChannelPicker(channels=src.channels, pick=0)
    kws = KWS()
    # doa = DOA(rate=16000, chunks=20)
    alexa = Alexa()

    # alexa.state_listener.on_listening = pixel_ring.listen
    # alexa.state_listener.on_thinking = pixel_ring.think
    # alexa.state_listener.on_speaking = pixel_ring.speak
    # alexa.state_listener.on_finished = pixel_ring.off
    
    src.link(ch0)
    ch0.link(kws)
    kws.link(alexa)

    # src.link(doa)

    def on_detected(keyword):
        # direction = doa.get_direction()
        alexa.listen()
        # pixel_ring.wakeup((direction + 0) % 360)
        # print('detected {} at direction {}'.format(keyword, direction))
        print('detected keyword')

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
