# -*- coding: utf-8 -*-
"""Audio source using pyaudio"""

import logging
import pyaudio

from .element import Element

logger = logging.getLogger(__file__)


class Source(Element):
    def __init__(self, rate=16000, frames_size=None, channels=None, device_name=None, bits_per_sample=16):
        """Setup a pyaudio callback stream to record audio

        Args:
            rate: sample rate
            frames_size: number of each channel's frames per chunk
            channels: channels' number
            device_name: device name to search
            bits_per_sample: sample width - 8, 16, 24 or 32
        """
        super(Source, self).__init__()

        self.rate = rate
        self.frames_size = frames_size if frames_size else rate / 100
        self.channels = channels if channels else 1

        self.pyaudio_instance = pyaudio.PyAudio()

        formats = [pyaudio.paInt8, pyaudio.paInt16, pyaudio.paInt24, pyaudio.paInt32]
        width = formats[bits_per_sample / 8 - 1]

        # Search device by name
        if device_name:
            for i in range(self.pyaudio_instance.get_device_count()):
                dev = self.pyaudio_instance.get_device_info_by_index(i)
                name = dev['name'].encode('utf-8')
                logger.info('{}:{} with {} input channels'.format(i, name, dev['maxInputChannels']))
                if name.find(device_name) >= 0:
                    logger.info('Use {}'.format(name))
                    device_index = i
                    break
        else:
            device_index = self.pyaudio_instance.get_default_input_device_info()['index']

        if device_index is None:
            raise ValueError('Can not find an input device {}'.format(device_name))

        self.stream = self.pyaudio_instance.open(
            start=False,
            format=width,
            input_device_index=device_index,
            channels=self.channels,
            rate=int(self.rate),
            frames_per_buffer=int(self.frames_size),
            stream_callback=self._callback,
            input=True
        )

    def _callback(self, in_data, frame_count, time_info, status):
        """pyaudio stream callback"""
        super(Source, self).put(in_data)

        return None, pyaudio.paContinue

    def start(self):
        self.stream.start_stream()

    def stop(self):
        self.stream.stop_stream()
