from blockchain import Blockchain
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
#import block
from node import Node
import util
import wallet
#import transaction


### JUST A BASIC EXAMPLE OF A REST API WITH FLASK

app = Flask(__name__)
CORS(app)

#.......................................................................................

# Register
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("A NODE HAS BEEN REGISTERED", data)
    if data:       
        ip_port = data.get('ip_port')
        public_key_decoded = data.get('public_key')
        public_key = public_key_decoded.encode('utf-8')
        id = node.register_node_to_ring(ip_port, public_key)
        # ip_port = request.args.get('ip_port')
        # public_key = request.args.get('public_key')
        response = {'id': str(id)}
        node.print_ring()
        return jsonify(response), 200
    else:
        response = {"error"}
        return jsonify(response), 400

@app.route('/ring', methods=['PUT'])
def update_ring():
    data = request.get_json()
    print(data)
    if data:
        for n in data.get('ring'):
            id = n.get('id')
            ip_port = n.get('ip_port')
            public_key = n.get('public_key')
            node.add_to_ring(id, ip_port, public_key)
        # ip_port = request.args.get('ip_port')
        # public_key = request.args.get('public_key')
        node.print_ring()
        response = {"OK"}
        return jsonify(response), 200
    else:
        response = {"Error"}
        return jsonify(response), 400

# get all transactions in the blockchain
@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    # transactions = blockchain.transactions
    # response = {'transactions': transactions}
    response2 = {'transactions': 'yeee'}
    return jsonify(response2), 200

@app.route('/transactions/create', methods=['GET'])
def create_transaction():
    response2 = {'transactions': 'yeee'}
    return jsonify(response2), 200

# run it once fore every node

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    parser.add_argument('-b', '--bootstrap', action='store_true', help='Whether the node is the bootstrap node or not')
    parser.add_argument('-n', '--nodes', type=int, help='Number of nodes expected on the network')
    args = parser.parse_args()
    port = args.port
    blockchain = Blockchain()
    if (args.bootstrap == True):
        node = Node(True, args.nodes)
    else:
        node = Node(False)
    app.run(host='0.0.0.0', port=port)
