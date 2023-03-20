import ast
import datetime
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import requests

from block import Block
from node import Node
from transaction import Transaction
import util
import wallet



### JUST A BASIC EXAMPLE OF A REST API WITH FLASK

app = Flask(__name__)
CORS(app)

#.......................................................................................

# Register a node the the ring of the bootstrap node
@app.route('/register', methods=['POST'])
def register():
	data = request.get_json()
	if data:
		ip_port = data.get('ip_port')
		public_key_decoded = data.get('public_key')
		public_key = public_key_decoded.encode('utf-8')
		print("Trying to register a new node to the network...")
		id = node.register_node_to_ring(ip_port, public_key)
		# ip_port = request.args.get('ip_port')
		# public_key = request.args.get('public_key')
		response = {'id': str(id)}
		return jsonify(response), 200
	else:
		response = {'id' : "error"}
		return jsonify(response), 400

# Receive all ring data from the bootstrap node
@app.route('/ring', methods=['PUT'])
def update_ring():
	data = request.get_json()
	print("Just got ring data from bootstrap, adding it to the ring...")
	print(data)
	if data:
		for n in data.get('ring'):
			id = n.get('id')
			ip_port = n.get('ip_port')
			public_key = n.get('public_key')
			node.add_to_ring(id, ip_port, public_key)
			# ip_port = request.args.get('ip_port')
			# public_key = request.args.get('public_key')
		print("Ring update finished, the full ring is:")
		node.print_ring() 
		response = {'status' : "OK"}
		return jsonify(response), 200
	else:
		response = {'status' : "Error"}
		return jsonify(response), 400

# Get all transactions in the blockchain
@app.route('/transactions/get', methods=['GET'])
def get_transactions():
	# transactions = blockchain.transactions
	# response = {'transactions': transactions}
	response2 = {'transactions': 'yeee'}
	return jsonify(response2), 200

# Receive a new block from a node
@app.route('/block', methods=['POST'])
def receive_block():
	data = request.get_json()
	if data:
		print('Just received data for a new block, checking if it is valid...')
		block_data = ast.literal_eval(data.get('block'))
		print(block_data)
		previousHash = block_data['previousHash']
		nonce = block_data['nonce']
		timestamp = block_data['timestamp']		
		new_block = Block(previousHash, nonce, timestamp)
		
		transactions = block_data['transactions']
		for t in transactions:
			t_data = ast.literal_eval(t)
			sender_address = t_data['sender_address']
			recipient_address = t_data['recipient_address']
			amount = t_data['amount']
			transaction_inputs = t_data['transaction_inputs']
			transaction_outputs = t_data['transaction_outputs']
			new_transaction = Transaction(sender_address, recipient_address, amount,
										  transaction_inputs, transaction_outputs)
			new_block.add_transaction_to_block(new_transaction)
		if node.validate_block(new_block):
			print('Block is valid! Adding to the blockchain...')
			node.add_block_to_blockchain(new_block)
			response = {'status' : 'Block added to blockchain'}
			print(new_block)
			return jsonify(response, 200)
		else:
			response = {'status' : 'Error: block cannot be validated!'}
			return jsonify(response, 400)
		
# Receive a transaction from a node
@app.route('/transaction', methods=['POST'])
def receive_transaction():
	data = request.get_json()
	print("Just received data for a new transaction")
	if data:
		transaction = data.get('transaction')		
	response2 = {'transactions': 'yeee'}
	return jsonify(response2), 200

# Run it once for every node
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    parser.add_argument('-b', '--bootstrap', action='store_true', help='Whether the node is the bootstrap node or not')
    parser.add_argument('-n', '--nodes', type=int, help='Number of nodes expected on the network')
    args = parser.parse_args()
    port = args.port
    if (args.bootstrap == True):
        node = Node(True, args.nodes)
    else:
        node = Node(False)
        node.register_request()
    app.run(host='0.0.0.0', port=port)


