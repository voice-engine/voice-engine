# -*- coding: utf-8 -*-

"""
Building block
"""


class Element(object):
    def __init__(self):
        self.sinks = []

    def put(self, data):
        for sink in self.sinks:
            sink.put(data)

    def start(self):
        pass

    def stop(self):
        pass

    def link(self, sink):
        if hasattr(sink, 'put') and callable(sink.put):
            self.sinks.append(sink)
        else:
            raise ValueError('Not implement put() method')

    def unlink(self, sink):
        self.sinks.remove(sink)

    def recursive_start(self):
        def recursive_start_sink(s):
            # start downstream first
            if hasattr(s, 'sinks'):
                for sink in s.sinks:
                    recursive_start_sink(sink)

            s.start()

        recursive_start_sink(self)

    def recursive_stop(self):
        def recursive_stop_sink(s):
            # stop downstream first
            if hasattr(s, 'sinks'):
                for sink in s.sinks:
                    recursive_stop_sink(sink)

            s.stop()

        recursive_stop_sink(self)
