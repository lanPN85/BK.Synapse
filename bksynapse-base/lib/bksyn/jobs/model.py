import uuid
import os
import json
import toml
import shutil

from file_read_backwards import FileReadBackwards
from datetime import datetime
from marshmallow import Schema, fields, post_load


class NodeConfig:
    def __init__(self, id):
        self.id = id


class NodeConfigSchema(Schema):
    id = fields.Str()


class TrainingJobConfig:
    def __init__(self, dataset, valDataset, 
        dataLoader, nodes, model, backend='pytorch',
        epochs=50, nodeType='cpu',
        batchSize=32, valDataLoader=None,
        optimizer='sgd', learningRate=1e-3,
        snapshotInterval=5, gradNorm=None):
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
        self.gradNorm = gradNorm


class TrainingJobConfigSchema(Schema):
    backend = fields.Str()
    model = fields.Str()
    dataset = fields.Str()
    valDataset = fields.Str()
    dataLoader = fields.Str()
    valDataLoader = fields.Str(missing=None)
    nodes = fields.List(
        fields.Nested(NodeConfigSchema())
    )
    nodeType = fields.Str(missing=None)
    batchSize = fields.Int(missing=None)
    epochs = fields.Int(missing=None)
    snapshotInterval = fields.Int(missing=None)
    optimizer = fields.Str(missing=None)
    learningRate = fields.Float(missing=None)
    gradNorm = fields.Float(missing=None)

    @post_load
    def make_obj(self, data):
        return TrainingJobConfig(**data)


class TrainingJobMetric:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class TrainingJobMetricSchema(Schema):
    name = fields.Str()
    value = fields.Float()


class TrainingJobStatus:
    def __init__(self, state, 
        iter=0, totalIter=0, 
        epoch=0, message=None, 
        metrics=None, timestamp=None, 
        **kwargs):
        if metrics is None:
            metrics = []
        if timestamp is None:
            timestamp = datetime.now()

        self.state = state
        self.iter = iter
        self.totalIter = totalIter
        self.epoch = epoch
        self.message = message
        self.metrics = metrics
        self.timestamp = timestamp
    
    @property
    def isActive(self):
        return self.state in ('EVALUATING', 'TRAINING', 'EVALUATED', 'SETUP')

    @property
    def isStopped(self):
        return self.state in ('INTERRUPT', 'ERROR', 'FINISHED')


class TrainingJobStatusSchema(Schema):
    state = fields.Str()
    iter = fields.Int(missing=None)
    totalIter = fields.Int(missing=None)
    epoch = fields.Int(missing=None)
    error = fields.Str(missing=None)
    metrics = fields.List(fields.Nested(TrainingJobMetricSchema()))
    message = fields.Str(missing='')
    timestamp = fields.DateTime(missing=None)
    isActive = fields.Boolean()
    isStopped = fields.Boolean()

    @post_load
    def make_obj(self, data):
        return TrainingJobStatus(**data)


class TrainingJobMetadata:
    def __init__(self, createdAt=None, pid=None):
        if createdAt is None:
            createdAt = datetime.now()

        self.createdAt = createdAt
        self.pid = pid


class TrainingJobMetadataSchema(Schema):
    createdAt = fields.DateTime()
    pid = fields.Int(missing=None)


class TrainingJob:
    def __init__(self, id, config=None, meta=None):      
        self.id = id
        self.config = config
        self.meta = meta

    @classmethod
    def from_config(cls, config, meta):
        job_id = str(uuid.uuid4())
        return cls(job_id, config, meta)
    
    def copy(self):
        return TrainingJob(uuid.uuid4(), self.config)

    @property
    def path(self):
        return os.path.join(os.environ['BKSYN_DATA_ROOT'], 'jobs', self.id)

    @property
    def log_path(self):
        return os.path.join(self.path, 'logs')

    @property
    def snapshot_path(self):
        return os.path.join(self.path, 'snapshots')

    @property
    def meta_path(self):
        return os.path.join(self.path, '.bks.meta')

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
    def hvd_timeline_path(self):
        return os.path.join(self.output_path, 'timeline.json')

    @property
    def output_path(self):
        return os.path.join(self.path, 'output')

    @property
    def stop_lock_path(self):
        return os.path.join(self.path, 'stop.lock')

    @property
    def exists(self):
        return os.path.exists(self.path)

    def update_status(self, status):
        d = TrainingJobStatusSchema().dump(status).data
        with open(self.status_path, 'wt') as f:
            json.dump(d, f, indent=2)
        with open(self.history_path, 'at') as f:
            s = '''# ===Start===\n%s# ===End===\n\n''' % toml.dumps({'entry': [d]})
            f.write(s)

    def lock(self):
        with open(self.stop_lock_path, 'wt') as f:
            f.write('===')

    def unlock(self):
        if os.path.exists(self.stop_lock_path):
            os.remove(self.stop_lock_path)

    def get_snapshot_name(self, epoch):
        if self.config.backend == 'pytorch':
            return 'epoch-%d.pth' % (epoch)

    def get_status(self):
        if not os.path.exists(self.status_path):
            return TrainingJobStatus('CREATED')

        with open(self.status_path, 'rt') as f:
            d = json.load(f)
        return TrainingJobStatus(**d)

    def get_history(self):
        with open(self.history_path, 'rt') as f:
            ld = toml.load(f).get('entry', [])
            return list(map(lambda x: TrainingJobStatusSchema().load(x).data, ld))

    def get_history_iter(self):
        with open(self.history_path, 'rt') as f:
            group = []
            for line in f:
                line = line.strip()
                if line == '# ===Start===':
                    group = []
                elif line == '# ===End===':
                    s = '\n'.join(group)
                    try:
                        d = toml.loads(s)['entry'][0]
                        obj = TrainingJobStatusSchema().load(d).data
                        yield obj
                    except:
                        continue
                else:
                    group.append(line)


    def get_history_rev_iter(self):
        with FileReadBackwards(self.history_path, encoding="utf-8") as f:
            group = []
            for line in f:
                line = line.strip()
                if line == '# ===End===':
                    group = []
                elif line == '# ===Start===':
                    s = '\n'.join(reversed(group))
                    try:
                        d = toml.loads(s)['entry'][0]
                        obj = TrainingJobStatusSchema().load(d).data
                        yield obj
                    except:
                        continue
                else:
                    group.append(line)


    def clear_outputs(self):
        shutil.rmtree(self.output_path, ignore_errors=True)
        shutil.rmtree(self.log_path, ignore_errors=True)
        shutil.rmtree(self.snapshot_path, ignore_errors=True)
        os.makedirs(self.log_path, exist_ok=True)
        os.makedirs(self.snapshot_path, exist_ok=True)
        os.makedirs(self.output_path, exist_ok=True)
        status = TrainingJobStatus('CREATED')
        self.update_status(status)

    def save(self):
        os.makedirs(self.path, exist_ok=True)
        os.makedirs(self.log_path, exist_ok=True)
        os.makedirs(self.snapshot_path, exist_ok=True)
        os.makedirs(self.output_path, exist_ok=True)
        
        conf_dict = TrainingJobConfigSchema().dump(self.config).data
        with open(self.config_path, 'wt') as f:
            json.dump(conf_dict, f, indent=2)

        meta_dict = TrainingJobMetadataSchema().dump(self.meta).data
        with open(self.meta_path, 'wt') as f:
            json.dump(meta_dict, f, indent=2)
        
        if not os.path.exists(self.status_path):
            status = TrainingJobStatus('CREATED')
            self.update_status(status)

    def delete(self):
        shutil.rmtree(self.path)

    @classmethod
    def load(cls, job_id):
        job = cls(job_id)
        with open(job.config_path, 'rt') as f:
            job.config = TrainingJobConfig(**json.load(f))
        with open(job.meta_path, 'rt') as f:
            job.meta = TrainingJobMetadataSchema().load(json.load(f)).data
        return job


class TrainingJobSchema(Schema):
    id = fields.Str()
    config = fields.Nested(TrainingJobConfigSchema())
    meta = fields.Nested(TrainingJobMetadataSchema())

    @post_load
    def make_obj(self, data):
        return TrainingJob(**data)
