"""
Compare Keyword Search (KWS) between audio with Noise Suppresion (NS) and raw audio.

The keyword is "snowboy". Channel 0 has NS, channel 1 doesn't.
"""


import time
from voice_engine.source import Source
from voice_engine.route import Route
from voice_engine.ns import NS
from voice_engine.kws import KWS


def main():
    src = Source(rate=16000, channels=2)
    route = Route(channels=src.channels)
    ns = NS(rate=16000, channels=1)

    def get_kws_callback(channel):
        def on_detected(keyword):
            print('detected @ {}'.format(channel))

        return on_detected

    kws = []
    for channel in range(2):
        k = KWS(model='snowboy', sensitivity=0.6, verbose=False)
        k.on_detected = get_kws_callback(channel)
        
        kws.append(k)

    # data flow between elements
    # ---------------------------
    # src -> route -> ns -> kws[0]
    #           \
    #           kws[1]
    src.link(route)
    route.link((ns, kws[1]))
    ns.link(kws[0])

    src.recursive_start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()
