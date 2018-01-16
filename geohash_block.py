import geohash
from nio.properties import BoolProperty, FloatProperty, \
                           IntProperty, VersionProperty
from nio.block.base import Block
from nio.util.discovery import not_discoverable
from enum import Enum


class Geohash(Block):

    version = VersionProperty("1.0.0")
    adj = BoolProperty(title='Neighbors', default=False)
    precision = IntProperty(title='Precision', default=6)
    lat = FloatProperty(title='Latitude', default=39.9195989)
    lng = FloatProperty(title='Longitude', default=-105.1095472)

    def process_signals(self, signals, input_id='default'):
        output_signals = []

        for signal in signals:
            precision = self.precision()
            lat = self.lat(signal)
            lng = self.lng(signal)

            loc = geohash.encode(lat, lng, precision)
            setattr(signal, 'results', loc)
            print(signal)
            if self.adj():
                neighbors = geohash.neighbors(loc)
                setattr(signal, 'neighbors', neighbors)

        self.notify_signals(signals)
