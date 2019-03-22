import uuid
import os
import json
import toml

from marshmallow import Schema, fields, post_load


class NodeConfig:
    def __init__(self, name):
        self.name = name


class NodeConfigSchema(Schema):
    name = fields.Str()


class TrainingJobConfig:
    def __init__(self, dataset, valDataset, 
        dataLoader, nodes, model, backend='pytorch',
        epochs=50, nodeType='cpu',
        batchSize=32, valDataLoader=None,
        optimizer='sgd', learningRate=1e-3,
        snapshotInterval=5):
        if valDataLoader is None:
            valDataLoader = dataLoader

        self.backend = backend
        self.model = model
        self.dataset = dataset
        self.valDataset = valDataset
        self.dataLoader = dataLoader
        self.valDataLoader = valDataLoader
        self.nodes = nodes
        self.epochs = epochs
        self.batchSize = batchSize
        self.nodeType = nodeType
        self.optimizer = optimizer
        self.learningRate = learningRate
        self.snapshotInterval = snapshotInterval


class TrainingJobConfigSchema(Schema):
    backend = fields.Str()
    model = fields.Str()
    dataset = fields.Str()
    valDataset = fields.Str()
    dataLoader = fields.Str()
    valDataLoader = fields.Str()
    nodes = fields.List(
        fields.Nested(NodeConfigSchema())
    )
    nodeType = fields.Str()
    batchSize = fields.Int()
    epochs = fields.Int()
    snapshotInterval = fields.Int()
    optimizer = fields.Str()
    learningRate = fields.Float()

    @post_load
    def make_obj(self, data):
        return TrainingJobConfig(**data)


class TrainingJobStatus:
    def __init__(self, state, 
        iter=0, totalIter=0, 
        epoch=0, message=None, 
        metrics=None):
        if metrics is None:
            metrics = {}

        self.state = state
        self.iter = iter
        self.totalIter = totalIter
        self.epoch = epoch
        self.message = message
        self.metrics = metrics


class TrainingJobStatusSchema(Schema):
    state = fields.Str()
    iter = fields.Int()
    totalIter = fields.Int()
    epoch = fields.Int()
    error = fields.Str()
    metrics = fields.Dict()

    @post_load
    def make_obj(self, data):
        return TrainingJobStatus(**data)


class TrainingJob:
    def __init__(self, id, config=None):      
        self.id = id
        self.config = config

    @classmethod
    def from_config(cls, config):
        job_id = uuid.uuid4()
        return cls(job_id, config)
    
    def copy(self):
        return TrainingJob(uuid.uuid4(), self.config)

    @property
    def path(self):
        return os.path.join(os.environ['BKDIGITS_DATA_ROOT'], 'jobs', self.id)

    @property
    def log_path(self):
        return os.path.join(self.path, 'logs')

    @property
    def snapshot_path(self):
        return os.path.join(self.path, 'snapshots')

    @property
    def config_path(self):
        return os.path.join(self.path, 'config.json')

    @property
    def status_path(self):
        return os.path.join(self.path, 'status.json')

    @property
    def history_path(self):
        return os.path.join(self.output_path, 'history.toml')

    @property
    def output_path(self):
        return os.path.join(self.path, 'output')

    @property
    def exists(self):
        return os.path.exists(self.path)

    def update_status(self, status):
        d = TrainingJobStatusSchema().dump(status).data
        with open(self.status_path, 'wt') as f:
            json.dump(d, f, indent=2)
        with open(self.history_path, 'at') as f:
            s = '%s\n\n' % toml.dumps({'entry': [d]})
            f.write(s)

    def get_status(self):
        with open(self.status_path, 'rt') as f:
            d = json.load(f)
        return TrainingJobStatusSchema().load(d).data

    def get_history(self):
        with open(self.history_path, 'rt') as f:
            return toml.load(f).get('entry', [])

    def save(self):
        os.makedirs(self.path)
        os.makedirs(self.log_path)
        os.makedirs(self.snapshot_path)
        
        conf_dict = TrainingJobConfigSchema().dump(self.config).data
        with open(self.config_path, 'wt') as f:
            json.dump(conf_dict, f, indent=2)

    @classmethod
    def load(cls, job_id):
        job = cls(job_id)
        with open(job.config_path, 'rt') as f:
            job.config = TrainingJobConfigSchema().load(json.load(f)).data
        return job

class TrainingJobSchema(Schema):
    id = fields.Str()
    config = fields.Nested(TrainingJobConfigSchema())

    @post_load
    def make_obj(self, data):
        return TrainingJob(**data)
