import flask
import os
import signal
import logging

from flask import current_app
from flask_restful import Resource
from subprocess import Popen

from apis import utils
from apis.logs import err_logged
from bksyn.jobs.model import TrainingJobConfig, TrainingJobConfigSchema,\
    TrainingJob, TrainingJobMetadata, TrainingJobMetadataSchema
from bksyn.nodes import Node, NodeDbClient


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


class DeleteTrainingJob(Resource):
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

        job.delete()
        return {
            'msg': 'Success'
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
        db_client = NodeDbClient.from_env()
        host_list = ['localhost:1']
        remote_workers = 0
        for node_conf in job.config.nodes:
            node_id = node_conf['id']
            node = db_client.get_node_by_id(node_id)
            if node is None:
                continue
            if not node.isActive:
                continue

            num_procs = 1
            if node.info['nodeType'] == 'gpu':
                num_procs = len(node.info['gpu'])
            remote_workers += num_procs
            host_list.append('%s:%d' % (node.info['address'], num_procs))

        host_str = ','.join(host_list)
        workers = 1 + remote_workers
        worker_exc = os.path.join(
            current_app.config['BACKEND_WORKER_DIRS'][job.config.backend], 'train.py')
        
        cmd = [
            'horovodrun -p 17992', 
            '-np', str(workers), '-H', host_str,
            worker_exc, '--job-id', job.id
        ]
        cmd = ' '.join(cmd)
        logger.debug(cmd)
        proc = Popen(cmd, shell=True)
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
