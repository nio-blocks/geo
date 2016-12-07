from geopy.location import Location
from collections import defaultdict
from unittest.mock import MagicMock
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..geocode_block import Geocode


class TestGeocodeBlock(NIOBlockTestCase):

    def test_default(self):
        """Default block config gets a location"""
        blk = Geocode()
        self.configure_block(blk, {})
        blk._geolocator = MagicMock()
        blk._geolocator.geocode.return_value = \
            Location('Test address', (1, 2), {"this": "is so raw"})
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        blk._geolocator.geocode.assert_called_once_with('175 5th Avenue NYC')
        self.assert_num_signals_notified(1)
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].location['address'], 'Test address')
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].location['latitude'], 1)
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].location['longitude'], 2)
        self.assertTrue(
            self.last_notified[DEFAULT_TERMINAL][0].location['raw'] is not None)

    def test_properties(self):
        """Use expression in query prop and non-default output_prop"""
        blk = Geocode()
        self.configure_block(blk, {"query": "{{ $address }}",
                                   "output_prop": "loc"})
        blk._geolocator = MagicMock()
        blk._geolocator.geocode.return_value = \
            Location('Test address', (1, 2), {"this": "is so raw"})
        blk.start()
        blk.process_signals([Signal({"address": "645 Harrison st, 94107"})])
        blk.stop()
        blk._geolocator.geocode.assert_called_once_with(
            '645 Harrison st, 94107')
        self.assert_num_signals_notified(1)
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].loc['address'], 'Test address')
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].loc['latitude'], 1)
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].loc['longitude'], 2)
        self.assertTrue(
            self.last_notified[DEFAULT_TERMINAL][0].loc['raw'] is not None)

    def test_bad_expr_property(self):
        """Use an invalid expression property config"""
        blk = Geocode()
        self.configure_block(blk, {"query": "{{ $bad_prop }}"})
        blk._geolocator = MagicMock()
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        self.assertEqual(blk._geolocator.geocode.call_count, 0)
        self.assert_num_signals_notified(1)
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].location, None)

    def test_bad_response(self):
        """Test when geocode does not return a reponse"""
        blk = Geocode()
        self.configure_block(blk, {})
        blk._geolocator = MagicMock()
        blk._geolocator.geocode.return_value = None
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        self.assertEqual(blk._geolocator.geocode.call_count, 1)
        self.assert_num_signals_notified(1)
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].location, None)

    def test_bad_request(self):
        """Test when geocode raises an exception"""
        blk = Geocode()
        self.configure_block(blk, {})
        blk._geolocator = MagicMock()
        blk._geolocator.geocode.side_effect = Exception
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        self.assertEqual(blk._geolocator.geocode.call_count, 1)
        self.assert_num_signals_notified(1)
        self.assertEqual(
            self.last_notified[DEFAULT_TERMINAL][0].location, None)
