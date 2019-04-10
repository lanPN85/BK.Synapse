import os
import json
import sys

from datetime import datetime
from marshmallow import Schema, fields, post_load


class DataLoader:
    def __init__(self, name, createdAt=None):
        if createdAt is None:
            createdAt = datetime.now()

        self.name = name
        self.createdAt = createdAt

    @property
    def path(self):
        return os.path.join(os.environ['BKSYN_DATA_ROOT'], 'dataloaders', self.name)

    @property
    def src_path(self):
        return os.path.join(self.path, 'src')

    @property
    def meta_path(self):
        return os.path.join(self.path, '.bks.meta')
    
    @property
    def loader_def_path(self):
        return os.path.join(self.src_path, 'bks_dataset.py')

    @property
    def exists(self):
        return os.path.exists(self.path)

    def get_dataset(self, dataset_path, val=False):
        dataset = None
        sys.path.insert(0, self.src_path)
        
        with open(self.loader_def_path, 'rt') as f:
            exec(f.read(), globals())
            if val:
                try:
                    dataset = UserValDataset(dataset_path)
                except NameError:
                    val = false

            if not val:
                dataset = UserDataset(dataset_path)
        
        # Avoid polluting path
        sys.path.remove(self.src_path)
        return dataset

    def save(self):
        os.makedirs(self.src_path, exist_ok=True)
        d = DataLoaderSchema().dump(self).data
        with open(self.meta_path, 'wt') as f:
            json.dump(d, f, indent=2)

    @classmethod
    def load(cls, name):
        dl = cls(name)
        try:
            with open(dl.meta_path, 'rt') as f:
                d = json.load(f)
        except FileNotFoundError:
            return None
        dl = DataLoaderSchema().load(d).data
        return dl


class DataLoaderSchema(Schema):
    name = fields.Str()
    createdAt = fields.DateTime()

    @post_load
    def make_obj(self, data):
        return DataLoader(**data)
