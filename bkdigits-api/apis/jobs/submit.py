import flask
import os
import signal
import logging

from flask import current_app
from flask_restful import Resource
from subprocess import Popen

from apis import utils
from apis.logs import err_logged
from bkdigits.jobs.model import TrainingJobConfig, TrainingJobConfigSchema, TrainingJob, TrainingJobMetadata, TrainingJobMetadataSchema


class SubmitTrainingJob(Resource):
    @err_logged
    def post(self):
        payload = flask.request.get_json()
        try:
            train_config = TrainingJobConfigSchema().load(payload).data
        except:
            return {
                'msg': 'Invalid config'
            }, 400

        meta = TrainingJobMetadata()
        job = TrainingJob.from_config(train_config, meta)
        job.save()

        return {
            'msg': 'Success',
            'job': {
                'id': job.id,
                'meta': TrainingJobMetadataSchema().dump(job.meta).data
            }
        }


class StartTrainingJob(Resource):
    @err_logged
    def post(self):
        logger = logging.getLogger('app')
        payload = flask.request.get_json()
        job_id = payload['job']['id']

        job = TrainingJob.load(job_id)
        if job is None:
            return {
                'msg': 'Invalid job ID'
            }, 400
        
        job.clear_outputs()
        job.unlock()

        # Spawn horovod subprocess
        host_list = ['localhost:1']
        for node in job.config.nodes:
            # TODO resolve node adressess
            pass
        host_str = ','.join(host_list)
        workers = 1
        worker_exc = os.path.join(
            current_app.config['BACKEND_WORKER_DIRS'][job.config.backend],
            'train.py')
        
        cmd = [
            'mpirun --allow-run-as-root', 
            '-np', str(workers), '-H', host_str,
            worker_exc, '--job-id', job.id
        ]
        cmd = ' '.join(cmd)
        logger.debug(cmd)
        proc = Popen(cmd, shell=True)
        job.meta['pid'] = proc.pid
        job.save()

        return {
            'msg': 'Success'
        }


class StopTrainingJob(Resource):
    @err_logged
    def post(self):
        payload = flask.request.get_json()
        job_id = payload['job']['id']

        job = TrainingJob.load(job_id)
        if job is None:
            return {
                'msg': 'Invalid job ID'
            }, 400
        
        job.lock()

        return {
            'msg': 'Success'
        }
