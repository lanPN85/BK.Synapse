import flask
import os
import shutil

from flask import current_app
from flask_restful import Resource

from apis import utils
from apis.logs import err_logged
from bkdigits.jobs import TrainingJob, TrainingJobSchema, TrainingJobStatusSchema


ROOT_DIR = os.path.join(os.environ['BKDIGITS_DATA_ROOT'], 'jobs')

class ListJobs(Resource):
    @err_logged
    def get(self):
        max_count = flask.request.args.get('max_count', default=20, type=int)
        offset = flask.request.args.get('offset', default=0, type=int)
        id_only = flask.request.args.get('id_only', default='false') == 'true'
        active_only = flask.request.args.get('active_only', default='false') == 'true'

        ids = os.listdir(ROOT_DIR)
        ids = filter(lambda x: os.path.isdir(os.path.join(ROOT_DIR, x)), ids)
        ids = sorted(ids)
        if id_only:
            return {
                'jobs': ids
            }

        objs = []
        for id_ in ids:
            obj = TrainingJob.load(id_)
            status = obj.get_status()
            if active_only:
                if not status.is_active:
                    continue
            d = TrainingJobSchema().dump(obj).data
            d['status'] = TrainingJobStatusSchema().dump(status).data
            objs.append(d)
        objs = objs[offset:offset + max_count]

        return {
            'jobs': objs
        }


class ListOptimizers(Resource):
    @err_logged
    def get(self):
        return {
            'optimizers': [
                {'value': 'sgd', 'text': 'SGD'},
                {'value': 'adam', 'text': 'Adam'},
                {'value': 'adadelta', 'text': 'Adadelta'},
                {'value': 'rmsprop', 'text': 'RMSProp'},
            ]
        }
