from collections import defaultdict
from unittest.mock import MagicMock
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..geohash_block import Geohash


class TestGeohashBlock(NIOBlockTestCase):

    def test_no_neighbors(self):

        blk = Geohash()
        self.configure_block(blk, {
            'adj': False,
            'precision': 10,
            'lat': 39.9195989,
            'long': -105.1095472
        })

        blk.start()
        blk.process_signals([Signal()])
        blk.stop()

        self.assert_num_signals_notified(1)
        self.assertDictEqual(self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
                             {'results': '9xj705jsd0'})

    def test_neighbors(self):

        blk = Geohash()
        self.configure_block(blk, {
            'adj': True,
            'precision': 4,
            'lat': 39.9195989,
            'long': -105.1095472
        })

        blk.start()
        blk.process_signals([Signal()])
        blk.stop()

        self.assert_num_signals_notified(1)
        self.assertDictEqual(self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
                             {'results': '9xj7',
                              'neighbors': [
                                  '9xj5',
                                  '9xje',
                                  '9xj6',
                                  '9xj4',
                                  '9xjd',
                                  '9xjk',
                                  '9xjh',
                                  '9xjs'
                              ]
                              }
                             )
