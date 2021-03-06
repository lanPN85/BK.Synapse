import flask
import os
import shutil

from flask import current_app
from flask_restful import Resource

from apis import utils
from apis.logs import err_logged
from bksyn.datasets import Dataset, DatasetSchema


ROOT_DIR = os.path.join(os.environ['BKSYN_DATA_ROOT'], 'datasets')

class ListDatasets(Resource):
    @err_logged
    def get(self):
        # max_count = flask.request.args.get('max_count', default=20, type=int)
        offset = flask.request.args.get('offset', default=0, type=int)
        name_only = flask.request.args.get('name_only', default='false') == 'true'

        names = os.listdir(ROOT_DIR)
        names = filter(lambda x: os.path.isdir(os.path.join(ROOT_DIR, x)), names)
        names = sorted(names)
        if name_only:
            return {
                'datasets': names
            }

        names = names[offset:]
        objs = []
        for name in names:
            obj = Dataset.load(name)
            d = DatasetSchema().dump(obj).data
            objs.append(d)
        
        return {
            'datasets': objs
        }


class DatasetExists(Resource):
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
