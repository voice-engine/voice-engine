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

        for model_path in [resource_path, os.path.join(resource_path, 'models')]:
            builtin_model = os.path.join(model_path, '{}.umdl'.format(model))
            if os.path.isfile(builtin_model):
                model = builtin_model
                break
        self.detector = snowboydetect.SnowboyDetect(common_resource.encode(), model.encode())
        # self.detector.SetAudioGain(1)
        # self.detector.ApplyFrontend(True)
        self.detector.SetSensitivity(str(sensitivity).encode())

        self.queue = queue.Queue()
        self.done = False
        self.thread = None

        self.on_detected = None

    def put(self, data):
        self.queue.put(data)

    def start(self):
        self.done = False
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.done = True
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=3)

    def run(self):
        while not self.done:
            try:
                data = self.queue.get(timeout=1)
            except queue.Empty:
                break

            ans = self.detector.RunDetection(data)
            if ans > 0:
                if callable(self.on_detected):
                    self.on_detected(ans)

            # sys.stdout.write(str(ans+2))
            # sys.stdout.flush()
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
