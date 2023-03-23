from Crypto.Hash import SHA256
import datetime
import json

import blockchain
import transaction
import util

BLOCK_CAPACITY = 3
MINING_DIFFICULTY = 4

class Block:
	def __init__(self, previousHash, nonce=0, timestamp=datetime.datetime.now()):
		self.timestamp = timestamp
		self.previousHash = previousHash
		self.nonce = nonce
		self.transactions = []
		self.hash_block()
		
	def __str__(self):
		string = 'PREVIOUS HASH:' + str(self.previousHash) + '\n'
		string += 'BLOCK HASH: ' + self.hash + '\n'
		for transaction in self.transactions:
			string += str(transaction)
			string += '\n'
		return string

	def create_genesis(self, total_nodes, bootstrap_address):
		self.timestamp = datetime.datetime.now()
		starting_amount = 100 * total_nodes
		ts = transaction.Transaction('0', bootstrap_address, starting_amount,
									 [], [])
		self.add_transaction_to_block(ts)
		return ts.transaction_id
	
	def hash_block(self):
		#calculate self.hash
		self.hash = SHA256.new(self.to_json().encode()).hexdigest()

	def to_json(self):
		transactions_to_json = []
		for t in self.transactions:
			transactions_to_json.append(t.to_json())
		block = {'previousHash': self.previousHash,
				 'nonce': self.nonce,
				 'timestamp': str(self.timestamp),
				 'transactions': transactions_to_json
		}
		return json.dumps(block)


	def add_transaction_to_block(self, transaction):
		# Add a transaction to this block
		if len(self.transactions) < BLOCK_CAPACITY:
			self.transactions.append(transaction)

	def is_full(self):
		return len(self.transactions) == BLOCK_CAPACITY
		
	def print_timestamp(self):
		print('Timestamp:', self.timestamp)

	def mine(self):
		flag = False
		while not flag:
			self.nonce = util.generate_nonce()
			self.hash_block()
			flag = (self.hash[:MINING_DIFFICULTY] == '0'*MINING_DIFFICULTY)

if __name__ == '__main__':
	start = datetime.datetime.now()			
	block = Block(0, 0)
	block.mine()
	str = datetime.datetime.now() - start
	print('Done in', str)
