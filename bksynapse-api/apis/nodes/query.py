import flask
import os
import logging

from flask import current_app
from flask_restful import Resource

from apis import utils
from apis.logs import err_logged
from bksyn.nodes import Node, NodeExtSchema

ROOT_DIR = os.path.join(os.environ['BKSYN_DATA_ROOT'], 'nodes')


class GetNodeList(Resource):
    @err_logged
    def get(self):
        active_only = flask.request.args.get('active_only', 'false')
        active_only = active_only.lower() == 'true'

        ids = os.listdir(ROOT_DIR)
        ids = filter(lambda x: os.path.isdir(os.path.join(ROOT_DIR, x)), ids)
        ids = sorted(ids)
        nodes = map(lambda x: Node.load(x), ids)
        nodes = filter(lambda x: x is not None, nodes)

        if active_only:
            nodes = filter(lambda x: x.isActive, nodes)

        nodes = map(lambda x: NodeExtSchema().dump(x).data, nodes)
        nodes = list(nodes)

        return {
            'nodes': nodes
        }


class GetNodeStatus(Resource):
    @err_logged
    def get(self):
        node_id = flask.request.args['id']

        node = Node.load(node_id)

        if node is None:
            return {
                'msg': 'Node ID not found'
            }, 404
        
        return {
            'status': node.status,
            'isActive': node.isActive
        }
