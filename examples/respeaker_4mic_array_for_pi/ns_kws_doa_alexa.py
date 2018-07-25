"""
Record audio from a 4 microphone array, and then search the keyword "snowboy".
After finding the keyword, Direction Of Arrival (DOA) is estimated.

The hardware is respeaker 4 mic array for raspberry pi.
"""

import signal
import time
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.ns import NS
from voice_engine.kws import KWS
from voice_engine.doa_respeaker_4mic_array import DOA
from pixel_ring import pixel_ring
from gpiozero import LED
from avs.alexa import Alexa

power = LED(5)
power.on()


def main():
    src = Source(rate=16000, frames_size=160, channels=4)
    ch0 = ChannelPicker(channels=src.channels, pick=0)
    ns = NS(rate=src.rate, channels=1)
    kws = KWS()
    doa = DOA(rate=16000, chunks=50)
    alexa = Alexa()

    alexa.state_listener.on_listening = pixel_ring.listen
    alexa.state_listener.on_thinking = pixel_ring.think
    alexa.state_listener.on_speaking = pixel_ring.speak
    alexa.state_listener.on_finished = pixel_ring.off


    # data flow between elements
    # ---------------------------
    # src -> ns -> kws -> alexa
    #    \
    #    doa
    src.pipeline(ch0, ns, kws, alexa)

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
    pixel_ring.off()

    # wait a second to allow other threads to exit
    time.sleep(1)

if __name__ == '__main__':
    main()
