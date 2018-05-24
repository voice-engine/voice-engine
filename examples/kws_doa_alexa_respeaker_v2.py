"""
Record audio from a 6 microphone array, and then search the keyword "alexa".
After finding the keyword, Direction Of Arrival (DOA) is estimated.

Requirements:
    pip install voice-engine avs pixel_ring

Hardware:
    respeaker v2. 
"""

import signal
import time
from voice_engine.source import Source
from voice_engine.kws import KWS
from voice_engine.channel_picker import ChannelPicker
from voice_engine.doa_respeaker_v2_6mic_array import DOA
from avs.alexa import Alexa
from pixel_ring import pixel_ring
import mraa

power = mraa.Gpio(12)
time.sleep(1)
power.dir(mraa.DIR_OUT)
power.write(0)

pixel_ring.wakeup(0)
time.sleep(1)
pixel_ring.off()


def main():
    src = Source(rate=16000, frames_size=320, channels=8)
    ch0 = ChannelPicker(channels=src.channels, pick=0)
    kws = KWS(model='alexa', sensitivity=0.8)
    doa = DOA(rate=src.rate, chunks=20)
    alexa = Alexa()

    alexa.state_listener.on_listening = pixel_ring.listen
    alexa.state_listener.on_thinking = pixel_ring.think
    alexa.state_listener.on_speaking = pixel_ring.speak
    alexa.state_listener.on_finished = pixel_ring.off

    src.pipeline(ch0, kws, alexa)

    src.link(doa)

    def on_detected(keyword):
        direction = doa.get_direction()
        print('detected {} at direction {}'.format(keyword, direction))
        alexa.listen()
        pixel_ring.wakeup(direction)

    kws.on_detected = on_detected

    is_quit = []
    def signal_handler(sig, frame):
        is_quit.append(True)
        print('quit')
    signal.signal(signal.SIGINT, signal_handler)

    src.pipeline_start()
    while not is_quit:
        time.sleep(1)

    src.pipeline_stop()


if __name__ == '__main__':
    main()
