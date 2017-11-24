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

    def pipeline(self, *args):
        source = self
        for sink in args:
            source.link(sink)
            source = sink

        return self

    def pipeline_start(self):
        def recursive_start_sink(s):
            # start downstream first
            if hasattr(s, 'sinks'):
                for sink in s.sinks:
                    recursive_start_sink(sink)

            s.start()

        recursive_start_sink(self)

    recursive_start = pipeline_start

    def pipeline_stop(self):
        def recursive_stop_sink(s):
            # stop upstream first
            s.stop()
            if hasattr(s, 'sinks'):
                for sink in s.sinks:
                    recursive_stop_sink(sink)

        recursive_stop_sink(self)

    recursive_stop = pipeline_stop
