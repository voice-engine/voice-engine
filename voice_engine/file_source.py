# -*- coding: utf-8 -*-


import logging
import wave
import threading

from .element import Element

logger = logging.getLogger(__file__)


class Source(Element):
    def __init__(self, wav, frames_size=160):
        super(Source, self).__init__()

        self._wav = wave.open(wav, 'r')
        self.channels = self._wav.getnchannels()
        self.rate = self._wav.getframerate()
        self.frames_size = frames_size
        self.done = False

    def run(self):
        while not self.done:
            frames = self._wav.readframes(self.frames_size)
            if not frames:
                # self._wav.rewind()
                # continue

                self.done = True
                break
            else:
                frames_bytes = self._wav.getsampwidth() * self.channels * self.frames_size
                frames = frames.rjust(frames_bytes)

            super(Source, self).put(frames)

    def start(self):
        self.done = False

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.done = True

    def is_active(self):
        return not self.done
