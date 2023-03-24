import ast
from collections import deque
from copy import deepcopy
import requests
from threading import Event, Lock, Thread
import time
import datetime
import util

import block
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet


BOOTSTRAP_PORT = '5000'
BOOTSTRAP_IP = '192.168.0.4'

class Node:
	def __init__(self, is_bootstrap=False, nodes=5):
		#self.wallet
		self.chain = Blockchain()
		self.current_block = block.Block(0)
		self.block_buffer = deque()
		self.block_lock = Lock()
		self.chain_lock = Lock()
		
		self.nodes = nodes
		self.sender_address = util.get_ip()+':'+BOOTSTRAP_PORT
		self.create_wallet()
		self.unspent_transactions = []
		self.all_utxos = dict()
		self.ring = []
		self.mine_flag = Event()
		self.mine_thread = Thread(target=self.mine_block)
		self.mine_thread.start()
		if is_bootstrap:
			print("The bootstrap node has been created, nodes =", self.nodes)
			self.id = 0
			self.ring.append([0, util.get_ip()+':'+BOOTSTRAP_PORT, self.wallet.public_key])
			genesis_transaction_id = self.current_block.create_genesis(self.nodes,
																	   self.sender_address)
			d = dict()
			d['id'] = genesis_transaction_id
			d['target'] = self.sender_address
			d['amount'] = 100 * self.nodes # 100 is a magic number
			self.unspent_transactions.append(d)
			self.all_utxos[self.sender_address] = self.unspent_transactions.copy()

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
				print('The node has already been registered')
				return

		self.ring.append([len(self.ring), ip_port, public_key])
		self.create_transaction(ip_port, 100, broadcast=False) # 100 is a magic number of starting NBCs

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
		self.print_ring()
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
		if self.chain.blocks:
			for block in self.chain.blocks:
				self.broadcast_block(self.chain.get_last_block(), genesis=True)
		self.broadcast_block(self.current_block, genesis=True)
	def add_to_ring(self, id, ip_port, public_key):
		self.ring.append([id, ip_port, public_key])
	
	def print_ring(self):
		for node in self.ring:
			print(node)
		print()

	def get_balance(self, ip_port):
		balance = 0
		for utxo in self.all_utxos[ip_port]:
			balance += utxo['amount']
		return balance

	def add_transaction_to_blockchain(self, transaction):
		#if enough transactions mine
		self.block_lock.acquire()
		self.current_block.add_transaction_to_block(transaction)
		if self.current_block.is_full():
			self.block_buffer.append(deepcopy(self.current_block))
			self.current_block = block.Block(0, 0)
			self.block_lock.release()
			self.mine_flag.set()
		else:
			self.block_lock.release()


	def mine_block(self):
		while True:
			self.mine_flag.wait()
			while self.block_buffer:
				print('Mining for a new block...')
				block_to_mine = self.block_buffer.popleft()
				self.chain_lock.acquire()
				if self.chain.get_last_block():
					block_to_mine.previousHash = self.chain.get_last_block().hash
				else:
					block_to_mine.previousHash = 0
				self.chain_lock.release()
				block_to_mine.hash_block()
				mine_time = time.time()
				block_to_mine.mine()
				mine_time = str(time.time() - mine_time) + '\n'
				print('Block successfuly mined!')
				file = open('mine_times.txt', 'a')
				file.write(mine_time)
				file.close()
				self.chain_lock.acquire()
				skip_flag = False
				if self.chain.get_last_block():
					for b in self.chain.blocks:
						for t1 in b.transactions:
							for t2 in block_to_mine.transactions:
								if t1.transaction_id == t2.transaction_id:
									skip_flag = True
									break
				self.chain_lock.release()
				if not skip_flag:
					self.chain.blocks.append(block_to_mine)
					self.broadcast_block(block_to_mine)
				else:
					print('I already have a similar block, skipping it...')
			self.mine_flag.clear()

	def filter_blocks(self):
		pass
		
	def broadcast_block(self, block, genesis=False):
		print('About to broadcast a new block to all the nodes in the network...')
		data = block.to_json()
		for node in self.ring:
			ip_port = node[1]
			if ip_port == self.sender_address:
				continue
			url = 'http://'+ip_port+'/receive_block'
			body = {'block' : data, 'all_utxos': self.all_utxos, 'genesis' : genesis}
			response = requests.post(url, json=body)
			if response:
				print('Node:', ip_port, ' HTTP code:', response.status_code)

	def validate_block(self, block):
		is_valid = self.chain.validate_block(block)
		return is_valid

	def add_block_to_blockchain(self, new_block, all_utxos, genesis=False):
		if genesis:
			self.current_block = new_block
			self.all_utxos = all_utxos
		else:
			for b in self.block_buffer:
				for buffer_t in b.transactions:
					for t in new_block.transactions:
						if buffer_t.transaction_id == t.transaction_id:
							print('Found transactions for a block I was about to mine')
			self.chain_lock.acquire()				
			self.chain.blocks.append(new_block)
			self.all_utxos = all_utxos
			self.chain_lock.release()
		

	
	def create_transaction(self, receiver_address, amount, broadcast=True):
		found = False
		for node in self.ring:
			if receiver_address == node[1]:
				found = True
		if not found:
			return False
		cur_sum = 0
		remaining = 0
		index = -1
		transaction_inputs = []
		for i, unspent_transaction in enumerate(self.all_utxos[self.sender_address]):
			cur_sum += unspent_transaction['amount']
			transaction_inputs.append(unspent_transaction['id'])
			if cur_sum >= amount:
				remaining = cur_sum - amount
				index = i
				break
		if cur_sum < amount:
			print('Cannot go forward with the transaction, not enough UTXOs in your wallet!')
			return False		 

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
		

		if index == len(self.all_utxos[self.sender_address]) - 1:
			self.all_utxos[self.sender_address] = [transaction_outputs[1]]
		else:
			self.all_utxos[self.sender_address] = self.all_utxos[self.sender_address][index+1:]
			self.all_utxos[self.sender_address].append(transaction_outputs[1])

		if not self.all_utxos.get(receiver_address):
			self.all_utxos[receiver_address] = []
		self.all_utxos[receiver_address].append(transaction_outputs[0])

		transaction.sign_transaction(self.wallet.private_key)

		if broadcast:
			self.broadcast_transaction(transaction)
		
		self.add_transaction_to_blockchain(transaction)
		return True
	
	def broadcast_transaction(self, transaction):
		print('About to broadcast a transaction to all nodes in the network...')
		data = transaction.to_json()
		for node in self.ring:
			ip_port = node[1]
			if ip_port == self.sender_address: # Don't send anything to myself
				continue
			url = 'http://'+ip_port+'/receive_transaction'
			body = {'transaction': data}
			response = requests.post(url, json=body)
			if response:
				print('Node:', ip_port, 'HTTP code:', response.status_code)


	def validate_transaction(self, transaction):
		sender = transaction.sender_address
		public_key = None
		for node in self.ring:
			if sender == node[1]:
				public_key = node[2]
				break
		if not transaction.verify_signature(public_key):
			print("Signature is not valid!")
			return False
		
		transaction_inputs = ast.literal_eval(transaction.transaction_inputs)
		transaction_outputs = ast.literal_eval(transaction.transaction_outputs)
		is_valid = False
		found = 0
		utxos_to_remove = []
		for t_input in transaction_inputs:
			for unspent in self.all_utxos[sender]:
				if t_input == unspent['id']:
					found += 1
					utxos_to_remove.append(unspent)
					break
		if found == len(transaction_inputs):
			for utxo in utxos_to_remove:
				self.all_utxos[sender].remove(utxo)
			for t_output in transaction_outputs:
				self.all_utxos[t_output['target']].append(t_output)
		return True		

#    def valid_proof(.., difficulty=MINING_DIFFICULTY):


	# Consensus functions

	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes
		pass

	def resolve_conflicts(self):
		#resolve correct chain
		pass


