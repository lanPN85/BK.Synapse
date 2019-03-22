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
from flask_jwt_extended import JWTManager

from apis.jobs import SubmitTrainingJob, StartTrainingJob, StopTrainingJob
from apis.models import SubmitModel, UploadModelSrc, UploadModelWeights


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
api.add_resource(SubmitModel, '/models/submit')
api.add_resource(UploadModelSrc, '/models/upload/<model_name>/src')
api.add_resource(UploadModelWeights, '/models/upload/<model_name>/weights')


def exit():
    pass

atexit.register(exit)

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'])
    print()
