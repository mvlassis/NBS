import block
import transaction

class Blockchain:
	def __init__(self):
		self.blocks = []

	def __str__(self):
		string = "BLOCKCHAIN:\n"
		for block in self.blocks:
			string += str(block) + '\n'
		return string

	def create_genesis(self, total_nodes, bootstrap_address):
		new_block = block.Block(1, 0)
		starting_amount = 100 * total_nodes
		ts = transaction.Transaction('0', bootstrap_address, starting_amount,
									 [], [])
		new_block.add_transaction_to_block(ts)
		self.blocks.append(new_block)
		print("Created genesis block")
		print(new_block)
		return ts.transaction_id

	def get_last_block(self):
		if self.blocks:
			return self.blocks[-1]
		else:
			return None

	def validate_block(self, new_block):
		is_valid = True
		# If the blockchain is NOT empty, check the hash of the previous block
		if self.blocks:
			if new_block.previousHash != self.get_last_block().hash:
				is_valid = False
		return is_valid
			
