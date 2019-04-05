import flask
import os
import shutil

from flask import current_app
from flask_restful import Resource

from apis import utils
from apis.logs import err_logged
from bksyn.loaders import DataLoader, DataLoaderSchema


class SubmitLoader(Resource):
    @err_logged
    def post(self):
        payload = flask.request.get_json()
        try:
            dl = DataLoaderSchema().load(payload).data
        except:
            return {
                'msg': 'Invalid payload'
            }, 400
        
        dl.save()
        return {
            'msg': 'Success'
        }, 200


class UploadLoaderSrc(Resource):
    @err_logged
    def post(self, loader_name):
        fp = flask.request.files['file']
        dl = DataLoader(loader_name)
        save_path = os.path.join(dl.src_path, 'src.zip')
        current_chunk = int(flask.request.form['dzchunkindex'])

        if current_chunk == 0 and os.path.exists(dl.src_path):
            shutil.rmtree(dl.src_path)
            os.makedirs(dl.src_path)

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


class DeleteLoader(Resource):
    @err_logged
    def post(self):
        payload = flask.request.get_json()
        dataset_name = payload['loader']['name']
        ds = DataLoader.load(dataset_name)

        if ds is None:
            return {
                'msg': 'Invalid loader name'
            }, 400
        
        shutil.rmtree(ds.path)
        return {
            'msg': 'Success'
        }

