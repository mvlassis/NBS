from Crypto.Hash import SHA256
import datetime
import json

import blockchain
import transaction

class Block:
	def __init__(self, previousHash, nonce, timestamp=datetime.datetime.now()):
		self.timestamp = timestamp
		self.previousHash = previousHash
		self.nonce = nonce
		self.transactions = []
		self.hash_block()
	def __str__(self):
		string = 'BLOCK HASH: ' + self.hash.hexdigest() + '\n'
		for transaction in self.transactions:
			string += str(transaction)
			string += '\n'
		return string
	
	def hash_block(self):
		#calculate self.hash
		self.hash = SHA256.new(self.to_json().encode())

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
		self.transactions.append(transaction)
		self.hash_block()
		
	def print_timestamp(self):
		print('Timestamp:', self.timestamp)
