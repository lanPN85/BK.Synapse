import flask
import os
import shutil

from flask import current_app
from flask_restful import Resource

from apis import utils
from apis.logs import err_logged
from bksyn.loaders import DataLoader, DataLoaderSchema


ROOT_DIR = os.path.join(os.environ['BKSYN_DATA_ROOT'], 'dataloaders')

class ListLoaders(Resource):
    @err_logged
    def get(self):
        max_count = flask.request.args.get('max_count', default=20, type=int)
        offset = flask.request.args.get('offset', default=0, type=int)
        name_only = flask.request.args.get('name_only', default='false') == 'true'

        names = os.listdir(ROOT_DIR)
        names = filter(lambda x: os.path.isdir(os.path.join(ROOT_DIR, x)), names)
        names = sorted(names)
        if name_only:
            return {
                'loaders': names
            }

        names = names[offset:offset + max_count]
        objs = []
        for name in names:
            obj = DataLoader(name)
            d = DataLoaderSchema().dump(obj).data
            objs.append(d)
        
        return {
            'loaders': objs
        }


class LoaderExists(Resource):
    @err_logged
    def get(self):
        name = flask.request.args('name')

        names = os.listdir(ROOT_DIR)
        names = filter(lambda x: os.path.isdir(os.path.join(ROOT_DIR, x)), names)
        names = list(names)
        exists = name in names

        return {
            'exists': str(exists).lower()
        }
