from geopy.location import Location
from collections import defaultdict
from unittest.mock import MagicMock
from nio.common.signal.base import Signal
from nio.util.support.block_test_case import NIOBlockTestCase
from ..geocode_block import Geocode


class TestGeocodeBlock(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        # This will keep a list of signals notified for each output
        self.last_notified = defaultdict(list)

    def signals_notified(self, signals, output_id='default'):
        self.last_notified[output_id].extend(signals)

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
            self.last_notified['default'][0].location.address, 'Test address')
        self.assertEqual(
            self.last_notified['default'][0].location.latitude, 1)
        self.assertEqual(
            self.last_notified['default'][0].location.longitude, 2)
        self.assertTrue(
            self.last_notified['default'][0].location.raw is not None)
