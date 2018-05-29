"""
Record 6 channels audio from the respeaker usb 4 mic array,
and then search the keyword "snowboy" at channel 0 and channel 1.
The audio of channel 0 is processed (AEC, beamforming, NS),
while channel 1 is raw audio data from a microphone.

The recorded audio is also saved as c6.wav.

The hardware is respeaker usb 4 mic array:
    https://www.seeedstudio.com/ReSpeaker-Mic-Array-v2.0-p-3053.html
"""


import time
from voice_engine.source import Source
from voice_engine.route import Route
from voice_engine.kws import KWS
from voice_engine.file_sink import FileSink


def main():
    src = Source(rate=16000, channels=6, device_name='hw:1')
    route = Route(channels=src.channels)

    def get_kws_callback(channel):
        def on_detected(keyword):
            print('detected @ {}'.format(channel))

        return on_detected

    kws = []
    for channel in range(2):
        k = KWS(model='snowboy', sensitivity=0.6)
        k.on_detected = get_kws_callback(channel)
        
        kws.append(k)


    sink = FileSink('c6.wav', rate=src.rate, channels=src.channels)

    src.pipeline(route, kws)
    src.link(sink)

    src.recursive_start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()
