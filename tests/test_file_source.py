"""
Read audio from a file, and then search the keyword "snowboy".
After finding the keyword, Direction Of Arrival (DOA) is estimated.
"""

import os
import time
from voice_engine.file_source import Source
from voice_engine.channel_picker import ChannelPicker


def test_file_source():
    src = Source(os.path.join(os.path.dirname(__file__), 'snowboy-alexa-8ch-16k.wav'))
    ch0 = ChannelPicker(channels=src.channels, pick=0)

    src.link(ch0)

    src.recursive_start()
    time.sleep(1)
    src.recursive_stop()
