# -*- coding: utf-8 -*-

import os

if os.system('which arecord >/dev/null') != 0:
    from .pyaudio_source import Source
else:
    from .alsa_source import Source

__all__ = ['Source']
