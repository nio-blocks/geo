from geopy.location import Location
from collections import defaultdict
from unittest.mock import MagicMock
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..reverse_geocode_block import ReverseGeocode


class TestReverseGeocodeBlock(NIOBlockTestCase):

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
            self.last_notified[DEFAULT_TERMINAL][0].location['address'],
            'Test address')
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].location['latitude'], 1)
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].location['longitude'], 2)
        raw_location = self.last_notified[DEFAULT_TERMINAL][0].location['raw']
        self.assertTrue(raw_location is not None)

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
            self.last_notified[DEFAULT_TERMINAL][0].loc['address'],
            'Test address')
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].loc['latitude'], 1)
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].loc['longitude'], 2)
        self.assertTrue(
            self.last_notified[DEFAULT_TERMINAL][0].loc['raw'] is not None)

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
            self.last_notified[DEFAULT_TERMINAL][0].location, None)

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
            self.last_notified[DEFAULT_TERMINAL][0].location, None)

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
            self.last_notified[DEFAULT_TERMINAL][0].location, None)

    def test_listed_results(self):
        """Geocoder may return a list of results, the first one is used."""
        blk = ReverseGeocode()
        self.configure_block(blk, {})
        blk._geolocator = MagicMock()
        blk._geolocator.reverse.return_value = [
            Location('foo', (1, 2), {"et": "cetera"}),
            Location('bar', (3, 4), {"et": "alia"})]
        blk.start()
        blk.process_signals([Signal({"lat": 3, "lng": 14})])
        blk.stop()
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].location['address'],
            'foo')
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].location['latitude'], 1)
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].location['longitude'], 2)
