import os
import sys
import json

from datetime import datetime
from marshmallow import Schema, fields, post_load


class Dataset:
    def __init__(self, name, createdAt=None, totalBytes=None):
        if createdAt is None:
            createdAt = datetime.now()

        self.name = name
        self.createdAt = createdAt
        self.totalBytes = totalBytes

    @property
    def path(self):
        return os.path.join(os.environ['BKSYN_DATA_ROOT'], 'datasets', self.name)
    
    @property
    def meta_path(self):
        return os.path.join(self.path, '.bks.meta')

    @property
    def exists(self):
        return os.path.exists(self.path)

    def update_size(self):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(self.path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        self.totalBytes = total_size

    def save(self):
        os.makedirs(self.path, exist_ok=True)
        d = DatasetSchema().dump(self).data
        with open(self.meta_path, 'wt') as f:
            json.dump(d, f, indent=2)

    @classmethod
    def load(cls, name):
        ds = cls(name)
        try:
            with open(ds.meta_path, 'rt') as f:
                d = json.load(f)
        except FileNotFoundError:
            return None
        ds = DatasetSchema().load(d).data
        return ds


class DatasetSchema(Schema):
    name = fields.Str()
    createdAt = fields.DateTime()
    totalBytes = fields.Int()

    @post_load
    def make_obj(self, data):
        return Dataset(**data)
