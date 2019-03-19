import os

from flask import current_app


def resolve_dataset_path(dataset_name):
    return os.path.join(current_app.config['DATA_ROOT'], 'datasets', dataset_name)

def resolve_loader_path(loader_name):
    return os.path.join(current_app.config['DATA_ROOT'], 'dataloaders', dataset_name)

def resolve_model_path(model_name):
    return os.path.join(current_app.config['DATA_ROOT'], 'models', dataset_name)

def resolve_job_path(job_name):
    return os.path.join(current_app.config['DATA_ROOT'], 'jobs', dataset_name)
