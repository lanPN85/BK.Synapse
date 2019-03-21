import unittest
import os
import sys
sys.path.append('.')
os.environ['BKDIGITS_DATA_ROOT'] = './tests/data'

from bkdigits.loaders import DataLoader
from bkdigits.datasets import Dataset as BkDigitsDataset


class TestLoaderModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loader = DataLoader('test')

    def test_get_dataset(self):
        ds = BkDigitsDataset('test')
        dataset = self.loader.get_dataset(ds.path)


if __name__ == "__main__":
    unittest.main()
