import unittest
import os
import sys
sys.path.append('.')
os.environ['BKDIGITS_DATA_ROOT'] = './tests/data'

from bkdigits.loaders import DataLoader as BkDigitsDataLoader
from bkdigits.datasets import Dataset as BkDigitsDataset
from bkdigits.models import Model
from bkdigits.jobs import TrainingJob


class TestJobModel(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
