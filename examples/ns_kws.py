"""

"""


import time
from voice_engine.source import Source
from voice_engine.kws import KWS
from voice_engine.ns import NS
from voice_engine.channel_picker import ChannelPicker


def main():
    src = Source(rate=16000, channels=2)
    ch1 = ChannelPicker(channels=2, pick=1)
    ns = NS(rate=16000, channels=1)
    kws = KWS(model='snowboy', sensitivity=0.6, verbose=True)

    src.pipeline(ch1, ns, kws)

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
