'''
To detect the keyword "snowboy" and translate the next sentence with Bing speech recognizer

Requirements:
    Get bing_speech_api.py from respeaker python library

    wget https://github.com/respeaker/respeaker_python_library/blob/master/respeaker/bing_speech_api.py
'''

import os
import sys
import threading
if sys.version_info[0] < 3:
    import Queue as queue
else:
    import queue

from voice_engine.element import Element
from bing_speech_api import BingSpeechAPI, RequestError


# put your bing key here
BING_KEY = ''


class Bing(Element):
    def __init__(self, key):
        super(Bing, self).__init__()

        self.key = key

        self.queue = queue.Queue()
        self.listening = False
        self.done = False
        self.event = threading.Event()

        self.bing = BingSpeechAPI(BING_KEY)

    def put(self, data):
        if self.listening:
            self.queue.put(data)

    def start(self):
        self.done = False
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.done = True

    def listen(self):
        self.listening = True
        self.event.set()

    def run(self):
        while not self.done:
            self.event.wait()

            def gen():
                count = 0
                while count < 16000 * 6:
                    data = self.queue.get()
                    if not data:
                        break

                    yield data
                    count += len(data) / 2
            
            # recognize speech using Microsoft Bing Voice Recognition
            try:
                # text = bing.recognize(gen(), language='zh-CN')
                text = self.bing.recognize(gen())
                print('Bing:{}'.format(text).encode('utf-8'))
            except ValueError:
                print('Not recognized')
            except RequestError as e:
                print('Network error {}'.format(e))

            self.listening = False
            self.event.clear()
            self.queue.queue.clear()


def main():
    import time
    from voice_engine.channel_picker import ChannelPicker
    from voice_engine.kws import KWS
    from voice_engine.source import Source

    src = Source(channels=2)
    ch0 = ChannelPicker(channels=src.channels, pick=0)
    kws = KWS(model='snowboy', sensitivity=0.7)
    bing = Bing(BING_KEY)

    src.pipeline(ch0, kws, bing)

    def on_detected(keyword):
        print('detected {}'.format(keyword))
        bing.listen()

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
