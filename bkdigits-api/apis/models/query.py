import flask
import os
import shutil

from flask import current_app
from flask_restful import Resource

from apis import utils
from apis.logs import err_logged
from bkdigits.models import Model, ModelSchema


ROOT_DIR = os.path.join(os.environ['BKDIGITS_DATA_ROOT'], 'models')

class ListModels(Resource):
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
                'models': names
            }

        names = names[offset:offset + max_count]
        objs = []
        for name in names:
            obj = Model.load(name)
            d = ModelSchema().dump(obj).data
            objs.append(d)
        
        return {
            'models': objs
        }


class ModelExists(Resource):
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
