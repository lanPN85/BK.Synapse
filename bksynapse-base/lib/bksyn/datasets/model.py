import os
import sys
import json

from marshmallow import Schema, fields, post_load


class Dataset:
    def __init__(self, name):
        self.name = name

    @property
    def path(self):
        return os.path.join(os.environ['BKSYN_DATA_ROOT'], 'datasets', self.name)
    
    @property
    def exists(self):
        return os.path.exists(self.path)

    def save(self):
        os.makedirs(self.path, exist_ok=True)


class DatasetSchema(Schema):
    name = fields.Str()

    @post_load
    def make_obj(self, data):
        return Dataset(**data)
