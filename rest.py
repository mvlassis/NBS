import ast
import datetime
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import requests

from blockchain import Blockchain
from block import Block
from node import Node
from transaction import Transaction
import util
import wallet

my_ip_port = util.get_ip()+':'+'5000'

### JUST A BASIC EXAMPLE OF A REST API WITH FLASK

app = Flask(__name__)
CORS(app)

#.......................................................................................

# Get the total balance of a user
@app.route('/balance', methods=['GET'])
def get_balance():
	balance = node.get_balance(my_ip_port)
	if balance >= 0:
		response = {'balance' : balance}
		return jsonify(response), 200
	else:
		response = {'balance' : 'An error occured'}
		return jsonify(response), 400

# Print the node's blockchain
@app.route('/blockchain', methods=['GET'])
def get_blockchain():
	blockchain = str(node.chain)
	response = {'blockchain' : blockchain}
	return jsonify(response), 200

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
	if data:
		for n in data.get('ring'):
			id = n.get('id')
			ip_port = n.get('ip_port')
			public_key = n.get('public_key').encode()
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
@app.route('/receive_block', methods=['POST'])
def receive_block():
	data = request.get_json()
	if data:
		print('Just received data for a new block, checking if it is valid...')
		block_data = ast.literal_eval(data.get('block'))
		
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
			print(new_block)
			print('Updating all utxos...')			
			all_utxos = data.get('all_utxos')
			node.all_utxos = all_utxos.copy()
			response = {'status' : 'Block added to blockchain'}
			return jsonify(response, 200)
		else:
			response = {'status' : 'Error: block cannot be validated!'}
			return jsonify(response, 400)

# Create a transaction and potentially broadcast it
@app.route('/create_transaction', methods=['POST'])
def create_transaction():
	data = request.get_json()
	if data:
		recipient = data.get('recipient')
		amount = int(data.get('amount'))
		if node.create_transaction(recipient, amount):
			response = {'status': 'Successful transaction'}
			return jsonify(response), 200
		else:
			response = {'status': 'Error'}
			return jsonify(response), 400
		
# Receive a transaction from a node and add it to the blockchain
@app.route('/receive_transaction', methods=['POST'])
def receive_transaction():
	data = request.get_json()
	if data:
		print("Just received data for a new transaction, checking to see if it is valid...")
		t_data = ast.literal_eval(data.get('transaction'))
		print('Transaction data', t_data)
		sender_address = t_data['sender_address']
		recipient_address = t_data['recipient_address']
		amount = t_data['amount']
		transaction_inputs = t_data['transaction_inputs']
		transaction_outputs = t_data['transaction_outputs']
		new_transaction = Transaction(sender_address, recipient_address, amount,
									  transaction_inputs, transaction_outputs)
		if node.validate_transaction(new_transaction):
			node.add_transaction_to_blockchain(new_transaction)
			response = 'Transaction is valid, added it to the blockchain'
			return response, 200
		else:
			resposne = 'Error when validating the transaction'
			return response, 400

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


