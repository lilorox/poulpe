import logging
import unittest
from unittest.mock import MagicMock, patch
from poulpe import Poulpe
from poulpe.exceptions import UnknownAssetException, UnknownAssetPairException

class PoupleTests(unittest.TestCase):
    def setUp(self):
        self.kraken_mock = MagicMock()

        # Mock the entire krakenex API object to better control the
        # return_values without calling the real API
        with patch.object(Poulpe, '_init_kraken_api', return_value=self.kraken_mock):
            self.p = Poulpe(None)


    def test_get_time_ok(self):
        self.kraken_mock.query_public.return_value = {
            'error': [],
            'result': {
                'rfc1123': 'Sun, 18 Dec 16 10:52:02 +0000',
                'unixtime': 1482058322
            }
        }

        assert self.p.get_time() == {
            'rfc1123': 'Sun, 18 Dec 16 10:52:02 +0000',
            'unixtime': 1482058322
        }


    def test_get_assets_ok(self):
        self.kraken_mock.query_public.return_value = {
            'error': [],
            'result': {
                'XXBT': {
                    'display_decimals': 5,
                    'altname': 'XBT',
                    'decimals': 10,
                    'aclass': 'currency'
                }
            }
        }

        assert self.p.get_assets(asset="XXBT") == {
            'XXBT': {
                'display_decimals': 5,
                'altname': 'XBT',
                'decimals': 10,
                'aclass': 'currency'
            }
        }


    def test_get_assets_UnknownAssetException(self):
        self.kraken_mock.query_public.return_value = {
            'error': ['EQuery:Unknown asset']
        }

        with self.assertRaises(UnknownAssetException):
            self.p.get_assets(asset="BadAsset")


    def test_get_asset_pairs_ok(self): pass

    def test_get_asset_pairs_bad_pair(self): pass

    def test_get_asset_pairs_bad_info(self): pass

    def test_get_ticker_ok_single_pair(self):
        self.kraken_mock.query_public.return_value = {
            'error': [],
            'result': {
                'XETHZEUR': {
                    'a': ['7.57141', '223', '223.000'],
                    'b': ['7.53001', '25', '25.000'],
                    'c': ['7.53000', '23.46440000'],
                    'h': ['7.59810', '7.60000'],
                    'l': ['7.36212', '7.22289'],
                    'o': '7.53000',
                    'p': ['7.49480', '7.39926'],
                    't': [326, 797],
                    'v': ['9613.35726598', '23372.76423418']
                }
            }
        }

        assert self.p.get_ticker(pairs="XETHZEUR") == {
            'XETHZEUR': {
                'a': ['7.57141', '223', '223.000'],
                'b': ['7.53001', '25', '25.000'],
                'c': ['7.53000', '23.46440000'],
                'h': ['7.59810', '7.60000'],
                'l': ['7.36212', '7.22289'],
                'o': '7.53000',
                'p': ['7.49480', '7.39926'],
                't': [326, 797],
                'v': ['9613.35726598', '23372.76423418']
            }
        }


    def test_get_ticker_ok_dual_pairs(self):
        self.kraken_mock.query_public.return_value = {
            'error': [],
            'result': {
                'XETHZEUR': {
                    'a': ['7.57141', '223', '223.000'],
                    'b': ['7.53001', '25', '25.000'],
                    'c': ['7.53000', '23.46440000'],
                    'h': ['7.59810', '7.60000'],
                    'l': ['7.36212', '7.22289'],
                    'o': '7.53000',
                    'p': ['7.49480', '7.39926'],
                    't': [326, 797],
                    'v': ['9613.35726598', '23372.76423418']
                },
                'XXBTZEUR': {
                    'a': ['755.69500', '2', '2.000'],
                    'b': ['755.69000', '2', '2.000'],
                    'c': ['755.69500', '0.12255285'],
                    'h': ['760.98000', '760.99000'],
                    'l': ['754.10100', '754.10100'],
                    'o': '759.80000',
                    'p': ['758.35990', '759.12163'],
                    't': [1340, 3070],
                    'v': ['761.69686329', '1609.76736165']
                }
            }
        }

        assert self.p.get_ticker(pairs="XETHZEUR,XXBTZEUR") == {
            'XETHZEUR': {
                'a': ['7.57141', '223', '223.000'],
                'b': ['7.53001', '25', '25.000'],
                'c': ['7.53000', '23.46440000'],
                'h': ['7.59810', '7.60000'],
                'l': ['7.36212', '7.22289'],
                'o': '7.53000',
                'p': ['7.49480', '7.39926'],
                't': [326, 797],
                'v': ['9613.35726598', '23372.76423418']
            },
            'XXBTZEUR': {
                'a': ['755.69500', '2', '2.000'],
                'b': ['755.69000', '2', '2.000'],
                'c': ['755.69500', '0.12255285'],
                'h': ['760.98000', '760.99000'],
                'l': ['754.10100', '754.10100'],
                'o': '759.80000',
                'p': ['758.35990', '759.12163'],
                't': [1340, 3070],
                'v': ['761.69686329', '1609.76736165']
            }
        }
        assert self.p.get_ticker(pairs="XETHZEUR,XXBTZEUR") == self.p.get_ticker(pairs=[ 'XETHZEUR', 'XXBTZEUR' ])


    def test_get_ticker_fail_UnknownAssetPairException(self):
        self.kraken_mock.query_public.return_value = {
            'error': ['EQuery:Unknown asset pair']
        }

        with self.assertRaises(UnknownAssetPairException):
            self.p.get_ticker(pairs="BadAssetPairs")


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main()
