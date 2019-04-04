import os
import json
import psutil
import GPUtil
import dateutil.parser

from datetime import datetime, timedelta
from marshmallow import Schema, post_load, fields


class Node:
    MAX_ALIVE_TIMEOUT = timedelta(seconds=21)

    def __init__(self, id, info=None, status=None, **kwargs):
        if status is None:
            status = {
                'lastUpdated': datetime.now().isoformat()
            }

        self.id = id
        self.info = info
        self.status = status

    @property
    def path(self):
        return os.path.join(os.environ['BKSYN_DATA_ROOT'], 'nodes', self.id)

    @property
    def status_path(self):
        return os.path.join(self.path, 'status.json')

    @property
    def info_path(self):
        return os.path.join(self.path, 'info.json')

    @property
    def isActive(self):
        lastUpdate = self.status.get('lastUpdated')
        
        if lastUpdate is None:
            return False
        lastUpdate = dateutil.parser.parse(lastUpdate)

        delta = datetime.now() - lastUpdate
        return delta < self.MAX_ALIVE_TIMEOUT

    @classmethod
    def from_env(cls, id):
        env = os.environ

        info = {
            'address': env['BKSYN_NODE_ADDRESS'],
            'nodeType': env['BKSYN_NODE_TYPE'],
            'memory': {
                'totalBytes': psutil.virtual_memory().total
            },
            'cpu': {
                'count': psutil.cpu_count(),
                'maxFreqMHz': psutil.cpu_freq().max
            }
        }

        if info['nodeType'] == 'gpu':
            gpus = GPUtil.getGPUs() 
            info['gpu'] = [{
                'totalMb': gpu.memoryTotal,
                'name': gpu.name
            } for gpu in gpus]

        return cls(id, info)

    def query_status(self):
        status = {
            'lastUpdated': datetime.now().isoformat(),
            'memory': {
                'usedBytes': psutil.virtual_memory().used
            },
            'cpu': {
                'percent': psutil.cpu_percent()
            }
        }

        if self.info['nodeType'] == 'gpu':
            gpus = GPUtil.getGPUs()
            status['gpu'] = [{
                'usedMb': gpu.memoryUsed,
                'load': gpu.load
            } for gpu in gpus]
        
        self.status = status

    def update_status(self):
        with open(self.status_path, 'wt') as f:
            json.dump(self.status, f, indent=2)

    def save(self):
        os.makedirs(self.path, exist_ok=True)
        with open(self.status_path, 'wt') as f:
            json.dump(self.status, f, indent=2)

        with open(self.info_path, 'wt') as f:
            json.dump(self.info, f, indent=2)

    @classmethod
    def load(cls, id):
        node = cls(id)

        try:
            with open(node.status_path, 'rt') as f:
                node.status = json.load(f)
            with open(node.info_path, 'rt') as f:
                node.info = json.load(f)
        except FileNotFoundError:
            return None
        
        return node


class NodeSchema(Schema):
    id = fields.Str()
    info = fields.Dict()
    status = fields.Dict()

    @post_load
    def make_obj(self, data):
        return Node(**data)


class NodeExtSchema(NodeSchema):
    isActive = fields.Boolean()

