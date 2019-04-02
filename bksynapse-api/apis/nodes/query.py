import flask
import os
import logging

from flask import current_app
from flask_restful import Resource

from apis import utils
from apis.logs import err_logged
from bksyn.nodes import Node, NodeDbClient, NodeExtSchema


class GetNodeList(Resource):
    @err_logged
    def get(self):
        active_only = flask.request.args.get('active_only', 'false')
        active_only = active_only.lower() == 'true'

        db_client = NodeDbClient.from_env()
        nodes = db_client.get_all_nodes()

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

        db_client = NodeDbClient.from_env()
        node = db_client.get_node_by_id(node_id)

        if node is None:
            return {
                'msg': 'Node ID not found'
            }, 404
        
        return {
            'status': node.status
        }
