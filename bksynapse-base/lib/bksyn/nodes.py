import os
import psutil
import GPUtil
import pymongo

from datetime import datetime, timedelta
from marshmallow import Schema, post_load, fields
from pymongo import MongoClient


class NodeDbClient(MongoClient):
    @classmethod
    def from_env(cls, **kwargs):
        env = os.environ
        return cls(env['BKSYN_NODEDB_HOST'], 
            int(env['BKSYN_NODEDB_PORT']), **kwargs)

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

    def get_all_nodes(self):
        cursor = self.collection.find(sort=[
            ('id', pymongo.ASCENDING)
        ])

        nodes = []
        for item in cursor:
            try:
                nd = NodeSchema().load(item).data
                nodes.append(nd)
            except:
                continue
        return nodes

    def get_node_by_id(self, id):
        node = self.collection.find_one({
            'id': id
        })

        if node is None:
            return None
        return NodeSchema().load(node).data


class Node:
    MAX_ALIVE_TIMEOUT = timedelta(seconds=21)

    def __init__(self, id, info, status=None, **kwargs):
        if status is None:
            status = {
                'lastUpdated': datetime.now().isoformat()
            }

        self.id = id
        self.info = info
        self.status = status

    @property
    def isActive(self):
        lastUpdate = self.status.get('lastUpdated')
        
        if lastUpdate is None:
            return False
        lastUpdate = datetime.strptime(lastUpdate, "%Y-%m-%dT%H:%M:%S")

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


class NodeSchema(Schema):
    id = fields.Str()
    info = fields.Dict()
    status = fields.Dict()

    @post_load
    def make_obj(self, data):
        return Node(**data)


class NodeExtSchema(NodeSchema):
    isActive = fields.Boolean()

