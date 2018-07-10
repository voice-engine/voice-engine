# -*- coding: utf-8 -*-
"""Audio source using ALSA `arecord`"""

import subprocess
import threading

from voice_engine.element import Element


class Source(Element):
    """Audio source that records audio using `arecord`

    `arecord` is spawned to write audio to the stdout pipe, and then record audio from the stdout pipe
    """

    def __init__(self, rate=16000, frames_size=None, channels=1, device_name='default', bits_per_sample=16):
        """Set parameters of recording

        Args:
            rate: sample rate
            frames_size: number of each channel's frames per chunk
            channels: channels' number
            device_name: ALSA PCM name, using `arecord -L` to get a list of PCM names
            bits_per_sample: sample width, 16 or 32
        """
        super(Source, self).__init__()

        self.rate = rate
        self.frames_size = frames_size if frames_size else int(rate / 100)
        self.channels = channels
        self.device_name = device_name
        self.format = ('S8', 'S16_LE', 'S24_LE', 'S32_LE')[int(bits_per_sample / 8) - 1]
        self.done = False
        self.thread = None

    def run(self):
        """Run `arecord` and read its stdout pipe"""
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
        """Start a recording thread"""
        self.done = False
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stop recording"""
        self.done = True
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=3)
