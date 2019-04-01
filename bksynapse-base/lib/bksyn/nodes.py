import os
import psutil
import GPUtil

from datetime import datetime
from marshmallow import Schema, post_load, fields
from pymongo import MongoClient


class NodeDbClient(MongoClient):
    @classmethod
    def from_env(cls, **kwargs):
        env = os.environ
        return cls(env['BKSYN_NODEDB_HOST'], 
            env['BKSYN_NODEDB_PORT'], **kwargs)

    @property
    def db(self):
        return self.bksyn

    @property
    def collection(self):
        return self.db.nodes

    def insert_node(self, node, exist_ok=False):
        d = NodeSchema().dump(node).data

        if not exist_ok:
            prev = self.collection.find_one({
                'id': node.id
            })
            if prev is not None:
                raise ValueError('Node with id `%s` already exists.' % node.id)
        
        return self.collection.insert_one(d)

    def remove_node(self, node):
        return self.collection.delete_one({
            'id': node.id
        })

    def update_node_status(self, node):
        return self.collection.update_one({
            'id': node.id
        }, {
            'status': node.status
        })


class Node:
    def __init__(self, id, info, status=None, **kwargs):
        if status is None:
            status = {
                'lastUpdated': datetime.now().isoformat()
            }

        self.id = id
        self.info = info
        self.status = status

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
            gpu = GPUtil.getGPUs()[0]
            info['gpu'] = {
                'totalMb': gpu.memoryTotal,
                'name': gpu.name
            }

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

        if info['nodeType'] == 'gpu':
            gpu = GPUtil.getGPUs()[0]
            status['gpu'] = {
                'usedMb': gpu.memoryUsed,
                'load': gpu.load
            }
        
        self.status = status


class NodeSchema(Schema):
    id = fields.Str()
    info = fields.Dict()
    status = fields.Dict()

    @post_load
    def make_obj(self, data):
        return Node(**data)


