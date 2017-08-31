"""
Hands-free Voice Assistant with Snowboy and Alexa Voice Service. The wake-up keyword is "alexa"

Requirement:
    pip install avs
"""


import time
import logging
from voice_engine.source import Source
from voice_engine.kws import KWS
from avs.alexa import Alexa


def main():
    logging.basicConfig(level=logging.DEBUG)

    src = Source(rate=16000)
    kws = KWS(model='alexa')
    alexa = Alexa()

    src.link(kws)
    kws.link(alexa)

    def on_detected(keyword):
        logging.info('detected {}'.format(keyword))
        alexa.listen()

    kws.set_callback(on_detected)

    src.recursive_start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()
