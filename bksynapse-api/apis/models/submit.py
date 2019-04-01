import flask
import os
import shutil

from flask import current_app
from flask_restful import Resource

from apis import utils
from apis.logs import err_logged
from bksyn.models import Model, ModelSchema


class SubmitModel(Resource):
    @err_logged
    def post(self):
        payload = flask.request.get_json()
        try:
            model = ModelSchema().load(payload).data
        except:
            return {
                'msg': 'Invalid payload'
            }, 400
        
        model.save()
        return {
            'msg': 'Success'
        }, 200


class UploadModelSrc(Resource):
    @err_logged
    def post(self, model_name):
        fp = flask.request.files['file']
        model = Model.load(model_name)
        save_path = os.path.join(model.src_path, 'src.zip')
        current_chunk = int(flask.request.form['dzchunkindex'])

        if current_chunk == 0 and os.path.exists(model.src_path):
            shutil.rmtree(model.src_path)
            os.makedirs(model.src_path)

        with open(save_path, 'ab') as f:
            f.seek(int(flask.request.form['dzchunkbyteoffset']))
            f.write(fp.stream.read())

        total_chunks = int(flask.request.form['dztotalchunkcount'])
        if current_chunk + 1 == total_chunks:
            utils.unzip(save_path)
            os.remove(save_path)

        return {
            'msg': 'Success'
        }


class UploadModelWeights(Resource):
    @err_logged
    def post(self, model_name):
        fp = flask.request.files['file']
        model = Model.load(model_name)
        save_path = os.path.join(model.path, 'weights.zip')
        current_chunk = int(flask.request.form['dzchunkindex'])

        with open(save_path, 'ab') as f:
            f.seek(int(flask.request.form['dzchunkbyteoffset']))
            f.write(fp.stream.read())

        total_chunks = int(flask.request.form['dztotalchunkcount'])
        if current_chunk + 1 == total_chunks:
            utils.unzip(save_path)
            os.remove(save_path)
        
        return {
            'msg': 'Success'
        }
