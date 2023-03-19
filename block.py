import blockchain
import datetime
import transaction

class Block:
	def __init__(self, previousHash, nonce):
		##set

		self.previousHash = previousHash
		self.timestamp = datetime.datetime.now()
		#self.hash
		#self.nonce
		self.transactions = []
        def create_genesis_block:
                transaction = Transaction("0", )
                return Block(previousHash = 1, nonce = 0)
	
	def myHash:
		#calculate self.hash


	def add_transaction(transaction transaction, blockchain blockchain):
		#add a transaction to the block
                
                
        def print_timestamp(self):
                print("Timestamp:", self.timestamp)
