import flask
import os

from flask import current_app
from flask_restful import Resource

from apis import utils
from apis.logs import err_logged
from bkdigits.jobs.model import TrainingJobConfig, TrainingJobConfigSchema


class SubmitTrainingJob(Resource):
    @err_logged
    def post(self):
        payload = flask.request.get_json()
        payload = TrainingJobConfigSchema().load(payload).data

        dataset_path = utils.resolve_dataset_path(payload.dataset)
        if not os.path.exists(dataset_path):
            return {
                'msg': 'Invalid dataset'
            }, 400
        val_dataset_path = utils.resolve_dataset_path(payload.valDataset)
        if not os.path.exists(val_dataset_path):
            return {
                'msg': 'Invalid validation dataset'
            }, 400
