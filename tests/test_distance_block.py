from collections import defaultdict
from ..geo_distance_block import GeoDistance
from nio.common.signal.base import Signal
from nio.util.support.block_test_case import NIOBlockTestCase


class TestDistanceBlock(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        # This will keep a list of signals notified for each output
        self.last_notified = defaultdict(list)

    def signals_notified(self, signals, output_id='default'):
        self.last_notified[output_id].extend(signals)

    def test_distance_vincenty(self):
        """ Make sure the Vincenty algorithm correctly adds data """

        # Examples taken from geopy website
        # http://geopy.readthedocs.org/en/latest/#module-geopy.distance
        blk = GeoDistance()
        self.configure_block(blk, {
            "point_1": {
                # Point 1 is Newport, RI
                # Try one with a string, one with a float
                "latitude": "41.49008",
                "longitude": -71.312796
            },
            "point_2": {
                # Point 2 will come from the signal
                "latitude": "{{ $lat }}",
                "longitude": "{{ $lng }}"
            },
            "distance_method": "Vincenty"
        })
        blk.start()
        blk.process_signals([Signal({
            # Point 2 will be Cleveland, OH
            # Try one with a string, one with a float
            "lat": 41.499498,
            "lng": "-81.695391"
        })])
        blk.stop()

        self.assert_num_signals_notified(1)
        self.assertAlmostEqual(
            self.last_notified['default'][0].geodata.miles, 538.3904, 2)

    def test_distance_great_circle(self):
        """ Make sure the Great Circle algorithm correctly adds data """
        blk = GeoDistance()
        self.configure_block(blk, {
            "point_1": {
                # Point 1 is Newport, RI
                # Try one with a string, one with a float
                "latitude": "41.49008",
                "longitude": -71.312796
            },
            "point_2": {
                # Point 2 will come from the signal
                "latitude": "{{ $lat }}",
                "longitude": "{{ $lng }}"
            },
            "distance_method": "GreatCircle"
        })
        blk.start()
        blk.process_signals([Signal({
            # Point 2 will be Cleveland, OH
            # Try one with a string, one with a float
            "lat": 41.499498,
            "lng": "-81.695391"
        })])
        blk.stop()

        self.assert_num_signals_notified(1)
        self.assertAlmostEqual(
            self.last_notified['default'][0].geodata.miles, 537.1485, 2)

    def test_missing_lat_lng(self):
        """ Make sure signals missing a lat/lng are handled """
        blk = GeoDistance()
        self.configure_block(blk, {
            "point_1": {
                "latitude": "41.49008",
                "longitude": -71.312796
            },
            "point_2": {
                # Point 2 will come from the signal
                "latitude": "{{ $lat }}",
                "longitude": "{{ $lng }}"
            }
        })
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()

        # We still want one signal
        self.assert_num_signals_notified(1)
        # We just don't want it to have the geodata
        self.assertFalse(hasattr(self.last_notified['default'][0], 'geodata'))

    def test_invalid_lat_lng(self):
        """ Make sure signals with an impossible lat/lng are handled """
        blk = GeoDistance()
        self.configure_block(blk, {
            "point_1": {
                "latitude": "41.49008",
                "longitude": -71.312796
            },
            "point_2": {
                # Point 2 will come from the signal
                "latitude": "{{ $lat }}",
                "longitude": "{{ $lng }}"
            },
            "distance_method": "GreatCircle"
        })
        blk.start()
        blk.process_signals([Signal({
            # Point 2 has an invalid lat/lng
            "lat": "not a number",
            "lng": "-810.111"
        })])
        blk.stop()

        # We still want one signal
        self.assert_num_signals_notified(1)
        # We just don't want it to have the geodata
        self.assertFalse(hasattr(self.last_notified['default'][0], 'geodata'))

    def test_custom_output(self):
        """ Tests that the output attribute can be configured """
        blk = GeoDistance()
        self.configure_block(blk, {
            "point_1": {
                # Point 1 is Newport, RI
                # Try one with a string, one with a float
                "latitude": "41.49008",
                "longitude": -71.312796
            },
            "point_2": {
                # Point 2 will come from the signal
                "latitude": "{{ $lat }}",
                "longitude": "{{ $lng }}"
            },
            "distance_method": "Vincenty",
            "output_prop": "custom"
        })
        blk.start()

        blk.process_signals([Signal({
            # Point 2 will be Cleveland, OH
            # Try one with a string, one with a float
            "lat": 41.499498,
            "lng": "-81.695391"
        })])

        blk.stop()

        # We should have one signal, but not with geodata this time
        self.assert_num_signals_notified(1)
        self.assertFalse(hasattr(self.last_notified['default'][0], 'geodata'))
        self.assertAlmostEqual(
            self.last_notified['default'][0].custom.miles, 538.3904, 2)

    def test_units(self):
        """ Make sure the correct units get added to the signal """

        # Examples taken from geopy website
        # http://geopy.readthedocs.org/en/latest/#module-geopy.distance
        blk = GeoDistance()
        self.configure_block(blk, {
            "point_1": {
                # Point 1 is Newport, RI
                # Try one with a string, one with a float
                "latitude": "41.49008",
                "longitude": -71.312796
            },
            "point_2": {
                # Point 2 will come from the signal
                "latitude": "{{ $lat }}",
                "longitude": "{{ $lng }}"
            },
            "distance_method": "Vincenty"
        })
        blk.start()
        blk.process_signals([Signal({
            # Point 2 will be Cleveland, OH
            # Try one with a string, one with a float
            "lat": 41.499498,
            "lng": "-81.695391"
        })])
        blk.stop()

        self.assert_num_signals_notified(1)
        out_signal = self.last_notified['default'][0]
        self.assertAlmostEqual(
            out_signal.geodata.miles, 538.3904451566326, 2)
        self.assertAlmostEqual(
            out_signal.geodata.feet, 538.3904451566326 * 5280, 1)
        self.assertAlmostEqual(
            out_signal.geodata.kilometers, 538.3904451566326 * 1.60934, 1)
        self.assertAlmostEqual(
            out_signal.geodata.meters, out_signal.geodata.kilometers * 1000, 1)
