import flask
import logging
import os
import traceback
import logging.config
import atexit

from flask import Flask
from flask_logconfig import LogConfig
from flask_cors import CORS
from flask_restful import Api

from apis.jobs import SubmitTrainingJob, StartTrainingJob, StopTrainingJob, ListJobs, ListOptimizers, GetJobStatus, DeleteTrainingJob
from apis.models import SubmitModel, UploadModelSrc, UploadModelWeights, ListModels, ModelExists
from apis.datasets import SubmitDataset, UploadDatasetFiles, ListDatasets, DatasetExists
from apis.loaders import SubmitLoader, UploadLoaderSrc, LoaderExists, ListLoaders
from apis.nodes import GetNodeList, GetNodeStatus


app = Flask(__name__)

# App configs
app.config.from_pyfile('configs/app.default.py')
CONFIG_ENVVAR = 'APP_CONF'
if CONFIG_ENVVAR in os.environ.keys():
    app.config.from_envvar(CONFIG_ENVVAR, silent=True)
logger = logging.getLogger('app')

# Modifiers
CORS(app)
LogConfig(app)
JWTManager(app)

# Add flask_restful endpoints
api = Api(app)
api.add_resource(SubmitTrainingJob, '/jobs/submit/training')
api.add_resource(StartTrainingJob, '/jobs/start/training')
api.add_resource(StopTrainingJob, '/jobs/stop/training')
api.add_resource(DeleteTrainingJob, '/jobs/delete/training')
api.add_resource(ListJobs, '/jobs/list')
api.add_resource(GetJobStatus, '/jobs/status')
api.add_resource(ListOptimizers, '/optimizers/list')

api.add_resource(SubmitModel, '/models/submit')
api.add_resource(UploadModelSrc, '/models/upload/<model_name>/src')
api.add_resource(UploadModelWeights, '/models/upload/<model_name>/weights')
api.add_resource(ListModels, '/models/list')
api.add_resource(ModelExists, '/models/exists')

api.add_resource(SubmitDataset, '/datasets/submit')
api.add_resource(UploadDatasetFiles, '/datasets/upload/<dataset_name>/files')
api.add_resource(ListDatasets, '/datasets/list')
api.add_resource(DatasetExists, '/datasets/exists')

api.add_resource(SubmitLoader, '/loaders/submit')
api.add_resource(UploadLoaderSrc, '/loaders/upload/<loader_name>/src')
api.add_resource(ListLoaders, '/loaders/list')
api.add_resource(LoaderExists, '/loaders/exists')

api.add_resource(GetNodeList, '/nodes/list')
api.add_resource(GetNodeStatus, '/nodes/status')


def exit():
    pass

atexit.register(exit)

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'])
    print()
