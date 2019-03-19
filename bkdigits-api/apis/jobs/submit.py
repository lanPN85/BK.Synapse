import flask
import os

from flask import current_app
from marshmallow import Schema, fields, post_load
from flask_restful import Resource

from apis import utils
from apis.logs import err_logged


class SubmitTrainingJobPayload:
    def __init__(self, dataset, val_dataset, dataloader, nodes, 
        backend='pytorch', shuffle=False, epochs=50, hooks=None):
        if hooks is None:
            hooks = []
        
        self.backend = backend
        self.dataset = dataset
        self.valDataset = val_dataset
        self.nodes = nodes
        self.shuffle = shuffle
        self.epochs = epochs
        self.hooks = hooks


class SubmitTrainingJobPayloadSchema(Schema):
    backend = fields.Str()
    dataset = fields.Str()
    valDataset = fields.Str()
    nodes = fields.List(fields.Str())
    shuffle = fields.Boolean()
    epochs = fields.Int()
    hooks = fields.List(fields.Str())

    @post_load
    def make_obj(self, data):
        return SubmitTrainingJobPayload(**data)

class SubmitTrainingJob(Resource):
    @err_logged
    def post(self):
        payload = flask.request.get_json()
        payload = SubmitTrainingJobPayloadSchema().load(payload).data

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
