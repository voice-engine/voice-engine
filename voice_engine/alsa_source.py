# -*- coding: utf-8 -*-

import os
import subprocess
import threading
from .element import Element


class Source(Element):
    def __init__(self, rate=16000, frames_size=None, channels=1, device_name='default', bits_per_sample=16):
        super(Source, self).__init__()

        self.rate = rate
        self.frames_size = frames_size if frames_size else int(rate / 100)
        self.channels = channels
        self.device_name = device_name
        self.format = ('S8', 'S16_LE', 'S24_LE', 'S32_LE')[int(bits_per_sample / 8) - 1]
        self.done = False
        self.thread = None

    def run(self):
        cmd = [
            'arecord',
            '-t', 'raw',
            '-f', self.format,
            '-c', str(self.channels),
            '-r', str(self.rate),
            '-D', self.device_name,
            '-q'
        ]
        print(cmd)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        frames_bytes = int(self.frames_size * self.channels * 2)
        while not self.done:
            audio = process.stdout.read(frames_bytes)
            super(Source, self).put(audio)

        process.kill()

    def start(self):
        self.done = False
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.done = True
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=3)

