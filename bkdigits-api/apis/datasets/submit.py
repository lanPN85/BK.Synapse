import flask
import os
import shutil

from flask import current_app
from flask_restful import Resource

from apis import utils
from apis.logs import err_logged
from bkdigits.datasets import Dataset, DatasetSchema


class SubmitDataset(Resource):
    @err_logged
    def post(self):
        payload = flask.request.get_json()
        try:
            ds = DatasetSchema().load(payload).data
        except:
            return {
                'msg': 'Invalid payload'
            }, 400
        
        ds.save()
        return {
            'msg': 'Success'
        }, 200


class UploadDatasetFiles(Resource):
    @err_logged
    def post(self, dataset_name):
        fp = flask.request.files['file']
        ds = Dataset(dataset_name)
        save_path = os.path.join(ds.path, 'files.zip')
        current_chunk = int(flask.request.form['dzchunkindex'])

        if current_chunk == 0 and os.path.exists(ds.path):
            shutil.rmtree(ds.path)
            os.makedirs(ds.path)

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
