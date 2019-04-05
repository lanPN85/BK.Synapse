import flask
import os
import time
import shutil

from flask import current_app
from flask_restful import Resource

from apis import utils
from apis.logs import err_logged
from bksyn.jobs import TrainingJob, TrainingJobSchema, TrainingJobStatusSchema, TrainingJobConfigSchema


ROOT_DIR = os.path.join(os.environ['BKSYN_DATA_ROOT'], 'jobs')


class ListJobs(Resource):
    @err_logged
    def get(self):
        # max_count = flask.request.args.get('max_count', default=20, type=int)
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
            max_retries = 30
            for i in range(max_retries):
                try:
                    status = obj.get_status()
                    break
                except Exception as e:
                    if i == (max_retries - 1):
                        return {
                            'msg': 'Can\'t get status'
                        }, 500
                time.sleep(0.5)
            if active_only:
                if not status['isActive']:
                    continue
            d = TrainingJobSchema().dump(obj).data
            d['status'] = TrainingJobStatusSchema().dump(status).data
            objs.append(d)
        objs = sorted(objs, key=lambda x: x['meta']['createdAt'], reverse=True)
        objs = objs[offset:]

        return {
            'jobs': objs
        }


class GetJobStatus(Resource):
    @err_logged
    def get(self):
        job_id = flask.request.args['id']
        job = TrainingJob.load(job_id)
        if job is None:
            return {
                'msg': 'Invalid job ID'
            }, 400
        
        max_retries = 30
        for i in range(max_retries):
            try:
                status = job.get_status()
                break
            except:
                if i == (max_retries - 1):
                    return {
                        'msg': 'Can\'t get status'
                    }, 500
                time.sleep(1)
        return {
            'status': TrainingJobStatusSchema().dump(status).data
        }


class GetJobConfig(Resource):
    @err_logged
    def get(self):
        job_id = flask.request.args['id']
        job = TrainingJob.load(job_id)
        if job is None:
            return {
                'msg': 'Invalid job ID'
            }, 400
        
        return {
            'info': TrainingJobConfigSchema().dump(job.info).data
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


class ExportJobOutput(Resource):
    @err_logged
    def get(self, job_id):
        job = TrainingJob.load(job_id)
        if job is None:
            return {
                'msg': 'Invalid job ID'
            }, 400

        if not os.path.exists(job.output_path):
            return {
                'msg': 'No output for requested job'
            }

        zip_path = os.path.join(job.path, 'output.zip')
        utils.zip(zip_path, job.output_path)

        return flask.send_from_directory(job.path, 'output.zip')
