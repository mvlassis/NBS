import argparse
import json
import requests

from blockchain import Blockchain
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
	print("Transaction")
	url = 'http://'+ my_ip_port + '/create_transaction'
	body = {'recipient' : args.recipient_address, 'amount': args.amount}
	response = requests.post(url, json=body)
	if response.status_code == 200:
		print("All OK!")
	else:
		print('An error occurred :(')
elif args.subcommand == "view":
	print("View")
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
	print("Help")
