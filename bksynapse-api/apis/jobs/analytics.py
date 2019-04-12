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
        
        # Get number of finished epochs
        finishedEpochs = 0
        for entry in job.get_history_rev_iter():
            if entry.state == 'EVALUATED':
                finishedEpochs = entry.epoch
                break
        
        # Get job time
        last_interval = next(job.get_history_rev_iter()).timestamp
        iterh = job.get_history_iter()
        first_interval = next(iterh).timestamp
        for entry in iterh:
            if entry.state == 'TRAINING':
                first_interval = entry.timestamp
                break
        elapsedSecs = (last_interval - first_interval).total_seconds()

        return {
            'summary': {
                'state': job.get_status().state,
                'finishedEpochs': finishedEpochs,
                'elapsedSecs': elapsedSecs
            }
        }


class GetPerEpochSummary(Resource):
    @err_logged
    def get(self):
        job_id = flask.request.args['id']
        job = TrainingJob.load(job_id)

        if job is None:
            return {
                'msg': 'Invalid job ID'
            }, 400

        epochs = []
        current_ep = 0
        current_obj = None
        for entry in job.get_history_iter():
            if (entry.state == 'TRAINING' and entry.epoch > current_ep) or entry.state == 'FINISHED':
                if current_obj is not None:
                    if 'startTime' in current_obj.keys() and 'endTime' in current_obj.keys():
                        current_obj['totalSecs'] = (current_obj['endTime'] - current_obj['startTime']).total_seconds()
                    current_obj.pop('startTime', None)
                    current_obj.pop('endTime', None)
                    epochs.append(current_obj)
                current_ep = entry.epoch
                current_obj = {}
                current_obj['startTime'] = entry.timestamp
            elif entry.state == 'EVALUATED':
                current_obj['metrics'] = entry.metrics
                current_obj['endTime'] = entry.timestamp
            elif entry.state == 'SAVING':
                current_obj['snapshot'] = job.get_snapshot_name(entry.epoch)
                current_obj['endTime'] = entry.timestamp

        return {
            'epochs': epochs
        }


