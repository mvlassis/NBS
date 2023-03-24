import argparse
import ast
import json
import requests

from block import Block
from blockchain import Blockchain
from transaction import Transaction
import util

status_code = 0 # used for testing purposes

my_ip_port = util.get_ip()+':'+'5000'

# Main parser
parser = argparse.ArgumentParser(description='CLI program for Noobcash')
subparsers = parser.add_subparsers(dest="subcommand", help= "Choose the specific subcommand to execute")

parser_t = subparsers.add_parser("t", help="Make a new transaction")
parser_view = subparsers.add_parser("view", help="View all transactions on the last block")
parser_balance = subparsers.add_parser("balance", help="Show the wallet balance")
parser_blockchain = subparsers.add_parser("blockchain", help="Show the blockchain")
parser_help = subparsers.add_parser("help", help="Help on all subcommands")

parser_t.add_argument("recipient_address", help="The public key of the wallet to send money to")
parser_t.add_argument("amount",  help="The amount in Noobcash")

args = parser.parse_args()

if args.subcommand == "t":
	url = 'http://'+ my_ip_port + '/create_transaction'
	body = {'recipient' : args.recipient_address, 'amount': args.amount}
	response = requests.post(url, json=body)
	if response.status_code == 200:
		print("All OK!")
	else:
		print('An error occurred :(')
elif args.subcommand == "view":
	print('Performing the "View" function')
	url = 'http://'+ my_ip_port + '/view_last_block'
	response = requests.get(url)
	if response.status_code == 200:
		print("All OK!")
		data = response.json()
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
		print(new_block)
	elif response.status_code == 204:
		print('No validated blocks yet!')
	else:
		print('An error occurred :(')
elif args.subcommand == "balance":
	url = 'http://'+ my_ip_port + '/balance'
	response = requests.get(url)
	if response:
		if response.status_code == 200:
			balance = response.json().get('balance')
			print('Balance:', balance, 'NBCs')
elif args.subcommand == 'blockchain':
	url = 'http://'+ my_ip_port + '/blockchain'
	response = requests.get(url)
	if response:
		if response.status_code == 200:
			blockchain = response.json().get('blockchain')
			print(blockchain)
elif args.subcommand == "help":
	message = '''USAGE: python cli.py <subcommand>, where subcommand can be one of:\n
- t <address> <amount> : Send <amount> to <address> (<address> must be a valid IP address + port)\n
- view                 : Show all transactions of the last validated block\n
- balance              : Show current balance of the wallet\n
- help                 : Show this message\n'''
	print(message)
