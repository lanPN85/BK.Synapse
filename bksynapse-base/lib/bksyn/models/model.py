import os
import json
import torch
import sys

from datetime import datetime
from marshmallow import Schema, fields, post_load


class Model:
    def __init__(self, name, backend='pytorch',
        dateCreated=None):
        if dateCreated is None:
            dateCreated = datetime.now()

        self.name = name
        self.backend = backend
        self.dateCreated = dateCreated

    @property
    def path(self):
        return os.path.join(os.environ['BKSYN_DATA_ROOT'], 'models', self.name)

    @property
    def src_path(self):
        return os.path.join(self.path, 'src')

    @property
    def model_def_path(self):
        return os.path.join(self.src_path, 'bkd_model.py')

    @property
    def exists(self):
        return os.path.exists(self.path)
    
    @property
    def meta_path(self):
        return os.path.join(self.path, 'meta.json')

    @property
    def weight_path(self):
        if self.backend == 'pytorch':
            return os.path.join(self.path, 'model.pth')

    @property
    def has_weights(self):
        return os.path.exists(self.weight_path)

    def load_model(self):
        model = None
        sys.path.insert(0, self.src_path)
        
        if self.backend == 'pytorch':
            with open(self.model_def_path, 'rt') as f:
                exec(f.read(), globals())
                _ = UserModel.loss
                model = UserModel()
            if self.has_weights:
                model.load_state_dict(torch.load(self.weight_path))
        
        # Avoid polluting path
        sys.path.remove(self.src_path)
        return model
    
    def save(self):
        os.makedirs(self.src_path, exist_ok=True)
        meta = ModelSchema().dump(self).data
        with open(self.meta_path, 'wt') as f:
            json.dump(meta, f, indent=2)

    @classmethod
    def load(cls, name):
        meta_path = cls(name).meta_path
        with open(meta_path, 'rt') as f:
            model = ModelSchema().load(json.load(f)).data
        return model


class ModelSchema(Schema):
    name = fields.Str()
    backend = fields.Str()
    dateCreated = fields.DateTime()

    @post_load
    def make_obj(self, data):
        return Model(**data)