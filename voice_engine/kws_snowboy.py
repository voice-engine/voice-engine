# -*- coding: utf-8 -*-

"""
Keyword spotting using snowboy
"""

import os
import sys
import threading
if sys.version_info[0] < 3:
    import Queue as queue
else:
    import queue

from snowboy import snowboydetect

from .element import Element


class KWS(Element):
    def __init__(self, model='snowboy', sensitivity=0.5):
        super(KWS, self).__init__()

        resource_path = os.path.join(os.path.dirname(snowboydetect.__file__), 'resources')
        common_resource = os.path.join(resource_path, 'common.res')
        if model in ['alexa', 'snowboy']:
            model = os.path.join(resource_path, '{}.umdl'.format(model))
        self.detector = snowboydetect.SnowboyDetect(common_resource, model)
        # self.detector.SetAudioGain(1)
        # self.detector.ApplyFrontend(True)
        self.detector.SetSensitivity(str(sensitivity).encode())

        self.queue = queue.Queue()
        self.done = False

        self.on_detected = None

    def put(self, data):
        self.queue.put(data)

    def start(self):
        self.done = False
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.done = True

    def run(self):
        while not self.done:
            data = self.queue.get()
            ans = self.detector.RunDetection(data)
            if ans > 0:
                if callable(self.on_detected):
                    self.on_detected(ans)

            super(KWS, self).put(data)

    def set_callback(self, callback):
        self.on_detected = callback


def main():
    import time
    from voice_engine.source import Source

    src = Source()
    kws = KWS()

    src.link(kws)

    def on_detected(keyword):
        print('found {}'.format(keyword))

    kws.on_detected = on_detected

    kws.start()
    src.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    kws.stop()
    src.stop()


if __name__ == '__main__':
    main()
