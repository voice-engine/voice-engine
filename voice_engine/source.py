# -*- coding: utf-8 -*-


import pyaudio
import logging

from .element import Element

logger = logging.getLogger(__file__)


class Source(Element):
    def __init__(self, rate=16000, frames_size=None, channels=None, device_index=None):

        super(Source, self).__init__()

        self.rate = rate
        self.frames_size = frames_size if frames_size else rate / 100
        self.channels = channels if channels else 1

        self.pyaudio_instance = pyaudio.PyAudio()

        if device_index is None:
            if channels:
                for i in range(self.pyaudio_instance.get_device_count()):
                    dev = self.pyaudio_instance.get_device_info_by_index(i)
                    name = dev['name'].encode('utf-8')
                    logger.info('{}:{} with {} input channels'.format(i, name, dev['maxInputChannels']))
                    if dev['maxInputChannels'] == channels:
                        logger.info('Use {}'.format(name))
                        device_index = i
                        break
            else:
                device_index = self.pyaudio_instance.get_default_input_device_info()['index']

            if device_index is None:
                raise ValueError('Can not find an input device with {} channel(s)'.format(channels))

        self.stream = self.pyaudio_instance.open(
            start=False,
            format=pyaudio.paInt16,
            input_device_index=device_index,
            channels=self.channels,
            rate=int(self.rate),
            frames_per_buffer=int(self.frames_size),
            stream_callback=self._callback,
            input=True
        )

    def _callback(self, in_data, frame_count, time_info, status):
        super(Source, self).put(in_data)

        return None, pyaudio.paContinue

    def start(self):
        self.stream.start_stream()

    def stop(self):
        self.stream.stop_stream()
