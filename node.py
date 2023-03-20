import requests
from threading import Thread
import time
import util

import block
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet


BOOTSTRAP_PORT = '5000'
BOOTSTRAP_IP = '192.168.0.4'

class Node:
	def __init__(self, is_bootstrap=False, nodes=5):
		##set

		#self.chain
		#self.current_id_count
		#self.NBCs
		#self.wallet
		self.chain = Blockchain()
		self.nodes = nodes
		self.sender_address = util.get_ip()+':'+BOOTSTRAP_PORT
		self.create_wallet()
		self.unspent_transactions = []
		self.all_utxos = dict()
		self.ring = []
		if is_bootstrap:
			print("The bootstrap node has been created, nodes =", self.nodes)
			self.id = 0
			self.ring.append([0, util.get_ip()+':'+BOOTSTRAP_PORT, self.wallet.public_key])
			genesis_transaction_id = self.chain.create_genesis(self.nodes, self.sender_address)
			d = dict()
			d['id'] = genesis_transaction_id
			d['target'] = self.sender_address
			d['amount'] = 100 * self.nodes # 100 is a magic number
			self.unspent_transactions.append(d)
			self.all_utxos[self.sender_address] = self.unspent_transactions.copy()
		#slef.ring[]   #here we store information for every node, as its id, its address (ip:port) its public key and its balance 

	def create_new_block():
		pass
		
	# Create a wallet for this node, with a public key and a private key
	def create_wallet(self):
		self.wallet = Wallet()

	def register_request(self):
		url = "http://"+BOOTSTRAP_IP+':'+BOOTSTRAP_PORT+"/register"
		body = {'ip_port': util.get_ip()+":"+BOOTSTRAP_PORT, 'public_key' : self.wallet.public_key.decode('utf-8')}
		response = requests.post(url, json=body)
		if response:
			self.id = response.json().get('id')
			print("Registered successfully to the network with id =", self.id)

	#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
	#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs
	def register_node_to_ring(self, ip_port, public_key):
		# Check if the node has been already registered
		for node in self.ring:
			if node[1] == ip_port:
				print("The node has already been registered")
				return

		self.create_transaction(ip_port, 100, broadcast=False) # 100 is a magic number of starting NBCs
		self.ring.append([len(self.ring), ip_port, public_key])
		print("A node has been registered and 100 NBCs have been transferred")
		
		# If all nodes have been registered, broadcast the whole ring, then
		# broadcast the genesis block
		if len(self.ring) == self.nodes:
			thread = Thread(target=self.broadcast_ring)
			thread.start()
		return len(self.ring)-1

	# Broadcast the ring to all members of the ring
	def broadcast_ring(self):
		time.sleep(3)
		data_body = [{"id": node[0], "ip_port": node[1], 'public_key': node[2].decode('utf-8')} for node in self.ring]
		print("About to broadcast the ring to all the nodes in the network...")
		for node in self.ring[1:]:
			ip_port = node[1]
			# url = "http://"+BOOTSTRAP_IP+':'+BOOTSTRAP_PORT+"/register"
			url = "http://"+ip_port+"/ring"
			body = {'ring' : data_body}
			response = requests.put(url, json=body)
			if response:
				print(response)
		self.broadcast_block(self.chain.get_last_block())
	def add_to_ring(self, id, ip_port, public_key):
		self.ring.append([id, ip_port, public_key])
	
	def print_ring(self):
		for node in self.ring:
			print(node)

	def create_transaction(self, receiver_address, amount, broadcast=True):
		# Remember to broadcast it
		cur_sum = 0
		remaining = 0
		index = -1
		transaction_inputs = []
		for i, unspent_transaction in enumerate(self.unspent_transactions):
			cur_sum += unspent_transaction['amount']
			transaction_inputs.append(unspent_transaction['id'])
			if cur_sum >= amount:
				remaining = cur_sum - amount
				index = i
				break
		if cur_sum < amount:
			print("Cannot go forward with the transaction, not enough UTXOs in your wallet!")
			return				 

		transaction = Transaction(self.sender_address, receiver_address, amount,
								  transaction_inputs)
		
		transaction_outputs = []
		d1 = dict()
		d1['id'] = transaction.transaction_id
		d1['target'] = receiver_address
		d1['amount'] = amount

		d2 = dict()
		d2['id'] = transaction.transaction_id
		d2['target'] = self.sender_address
		d2['amount'] = remaining
		transaction_outputs.append(d1)
		transaction_outputs.append(d2)
		
		transaction.transaction_outputs = transaction_outputs

		if index == len(self.unspent_transactions) - 1:
			self.unspent_transactions = [transaction_outputs[1]]
		else:
			self.unspent_transactions[index+1:]
			self.unspent_transactions.append[transactions_outputs[1]]

		if not self.all_utxos.get(self.sender_address):
			self.all_utxos[self.sender_address] = []
		self.all_utxos[self.sender_address] = self.unspent_transactions.copy()
		if not self.all_utxos.get(receiver_address):
			self.all_utxos[receiver_address] = []
		self.all_utxos[receiver_address].append(transaction_outputs[0])

		transaction.sign_transaction(self.wallet.private_key)

		if broadcast:
			self.broadcast_transaction(transaction)
		
		self.add_transaction_to_blockchain(transaction)
		


	def broadcast_transaction(self, transaction):
		print("About to broadcast a transaction")
		data = transaction.to_json()
		for node in self.ring:
			ip_port = node[1]
			if ip_port == self.sender_address:
				continue
			url = 'http://'+ip_port+'/transaction'
			body = {'transaction': data}
			response = requests.post(url, json=body)
			if response:
				print('Node:', ip_port, 'HTTP code:', response.status_code)


	def validate_transaction():
		#use of signature and NBCs balance
		pass

	def add_transaction_to_blockchain(self, transaction):
		#if enough transactions mine
		self.chain.get_last_block().add_transaction_to_block(transaction)


	def mine_block():
		pass


	def broadcast_block(self, block):
		print("About to broadcast a new block to all the nodes in the network...")
		data = block.to_json()
		for node in self.ring:
			ip_port = node[1]
			if ip_port == self.sender_address:
				continue
			url = 'http://'+ip_port+'/block'
			body = {'block' : data}
			response = requests.post(url, json=body)
			if response:
				print('Node:', ip_port, ' HTTP code:', response.status_code)

	def validate_block(self, block):
		is_valid = self.chain.validate_block(block)
		return is_valid

	def add_block_to_blockchain(self, block):
		self.chain.blocks.append(block)
		
		

#    def valid_proof(.., difficulty=MINING_DIFFICULTY):


	# Consensus functions

	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes
		pass

	def resolve_conflicts(self):
		#resolve correct chain
		pass


