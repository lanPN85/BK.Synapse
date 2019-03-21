import os
import json
import sys

from marshmallow import Schema, fields, post_load


class DataLoader:
    def __init__(self, name):
        self.name = name

    @property
    def path(self):
        return os.path.join(os.environ['BKDIGITS_DATA_ROOT'], 'dataloaders', self.name)

    @property
    def src_path(self):
        return os.path.join(self.path, 'src')
    
    @property
    def loader_def_path(self):
        return os.path.join(self.src_path, 'bkd_dataset.py')

    @property
    def exists(self):
        return os.path.exists(self.path)

    def get_dataset(self, dataset_path):
        model = None
        sys.path.insert(0, self.src_path)
        
        with open(self.loader_def_path, 'rt') as f:
            exec(f.read(), globals())
            _ = UserDataset.collate
            dataset = UserDataset(dataset_path)
        
        # Avoid polluting path
        sys.path.remove(self.src_path)
        return dataset

    def save(self):
        os.makedirs(self.path, exist_ok=True)
        with open(self.content_path, 'wt') as f:
            f.write(self.content)

    @classmethod
    def load(cls, name):
        loader = cls(name)
        with open(loader.content_path, 'rt') as f:
            loader.content = f.read()
        return loader


class DataLoaderSchema(Schema):
    name = fields.Str()

    @post_load
    def make_obj(self, data):
        return DataLoader(**data)