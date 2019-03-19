import os

from flask import current_app


def resolve_dataset_path(dataset_name):
    return os.path.join(current_app.config['DATASET_PATH'], dataset_name)
