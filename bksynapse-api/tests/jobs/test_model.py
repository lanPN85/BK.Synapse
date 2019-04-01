import unittest
import os
import sys
sys.path.append('.')
os.environ['BKSYN_DATA_ROOT'] = './tests/data'

from bksyn.loaders import DataLoader as BkDigitsDataLoader
from bksyn.datasets import Dataset as BkDigitsDataset
from bksyn.models import Model
from bksyn.jobs import TrainingJob


class TestJobModel(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
