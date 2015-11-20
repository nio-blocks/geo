from geopy.location import Location
from collections import defaultdict
from unittest.mock import MagicMock
from nio.common.signal.base import Signal
from nio.util.support.block_test_case import NIOBlockTestCase
from ..reverse_geocode_block import ReverseGeocode


class TestReverseGeocodeBlock(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        # This will keep a list of signals notified for each output
        self.last_notified = defaultdict(list)

    def signals_notified(self, signals, output_id='default'):
        self.last_notified[output_id].extend(signals)

    def test_default(self):
        """Default block config gets a location"""
        blk = ReverseGeocode()
        self.configure_block(blk, {})
        blk._geolocator = MagicMock()
        blk._geolocator.reverse.return_value = \
            Location('Test address', (1, 2), {"this": "is so raw"})
        blk.start()
        blk.process_signals([Signal({"lat": 3, "lng": 14})])
        blk.stop()
        blk._geolocator.reverse.assert_called_once_with((3, 14))
        self.assert_num_signals_notified(1)
        self.assertEqual(
            self.last_notified['default'][0].location.address, 'Test address')
        self.assertEqual(
            self.last_notified['default'][0].location.latitude, 1)
        self.assertEqual(
            self.last_notified['default'][0].location.longitude, 2)
        self.assertTrue(
            self.last_notified['default'][0].location.raw is not None)

    def test_properties(self):
        """Use expression in query prop and non-default output_prop"""
        blk = ReverseGeocode()
        self.configure_block(blk, {"output_prop": "loc"})
        blk._geolocator = MagicMock()
        blk._geolocator.reverse.return_value = \
            Location('Test address', (1, 2), {"this": "is so raw"})
        blk.start()
        blk.process_signals([Signal({"lat": 3, "lng": 14})])
        blk.stop()
        blk._geolocator.reverse.assert_called_once_with((3, 14))
        self.assert_num_signals_notified(1)
        self.assertEqual(
            self.last_notified['default'][0].loc.address, 'Test address')
        self.assertEqual(
            self.last_notified['default'][0].loc.latitude, 1)
        self.assertEqual(
            self.last_notified['default'][0].loc.longitude, 2)
        self.assertTrue(
            self.last_notified['default'][0].loc.raw is not None)

    def test_bad_expr_property(self):
        """Use an invalid expression property config"""
        blk = ReverseGeocode()
        self.configure_block(blk, {"location":
                                   {"latitude": "{{ $bad_prop }}",
                                    "longitude": "{{ $bad_prop }}"}})
        blk._geolocator = MagicMock()
        blk.start()
        blk.process_signals([Signal({"lat": 3, "lng": 14})])
        blk.stop()
        self.assertEqual(blk._geolocator.reverse.call_count, 0)
        self.assert_num_signals_notified(1)
        self.assertEqual(
            self.last_notified['default'][0].location, None)

    def test_bad_response(self):
        """Test when geocode does not return a reponse"""
        blk = ReverseGeocode()
        self.configure_block(blk, {})
        blk._geolocator = MagicMock()
        blk._geolocator.reverse.return_value = None
        blk.start()
        blk.process_signals([Signal({"lat": 3, "lng": 14})])
        blk.stop()
        self.assertEqual(blk._geolocator.reverse.call_count, 1)
        self.assert_num_signals_notified(1)
        self.assertEqual(
            self.last_notified['default'][0].location, None)

    def test_bad_request(self):
        """Test when geocode raises an exception"""
        blk = ReverseGeocode()
        self.configure_block(blk, {})
        blk._geolocator = MagicMock()
        blk._geolocator.reverse.side_effect = Exception
        blk.start()
        blk.process_signals([Signal({"lat": 3, "lng": 14})])
        blk.stop()
        self.assertEqual(blk._geolocator.reverse.call_count, 1)
        self.assert_num_signals_notified(1)
        self.assertEqual(
            self.last_notified['default'][0].location, None)
