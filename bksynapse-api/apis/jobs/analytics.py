import flask
import os
import time
import shutil

from flask import current_app
from flask_restful import Resource

from apis import utils
from apis.logs import err_logged
from bksyn.jobs import TrainingJob, TrainingJobStatusSchema


class GetJobSummary(Resource):
    @err_logged
    def get(self):
        job_id = flask.request.args['id']
        job = TrainingJob.load(job_id)

        if job is None:
            return {
                'msg': 'Invalid job ID'
            }, 400

        history = job.get_history()
        # history = list(map(lambda x: TrainingJobStatusSchema().load(x).data, history))
        
        # Get number of finished epochs
        finishedEpochs = 0
        for entry in reversed(history):
            entry = TrainingJobStatusSchema().load(entry).data
            if entry.state == 'EVALUATED':
                finishedEpochs = entry.epoch
                break
        
        # Get job time
        last_interval = TrainingJobStatusSchema().load(history[-1]).data.timestamp
        first_interval = TrainingJobStatusSchema().load(history[0]).data.timestamp
        for entry in history:
            entry = TrainingJobStatusSchema().load(entry).data
            if entry.state == 'TRAINING':
                first_interval = entry.timestamp
                break
        elapsedSecs = (last_interval - first_interval).total_seconds()

        return {
            'summary': {
                'state': job.get_status()['state'],
                'finishedEpochs': finishedEpochs,
                'elapsedSecs': elapsedSecs
            }
        }

