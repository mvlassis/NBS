import argparse
import csv
import json
import pandas
import mysql.connector

status_code = 0 # used for testing purposes

# Main parser
parser = argparse.ArgumentParser(description='CLI program for Noobcash')
subparsers = parser.add_subparsers(dest="subcommand", help= "Choose the specific subcommand to execute")

parser_t = subparsers.add_parser("t", help="Make a new transaction")
parser_view = subparsers.add_parser("view", help="View all transactions on the last block")
parser_balance = subparsers.add_parser("balance", help="Show the wallet balance")
parser_help = subparsers.add_parser("help", help="Help on all subcommands")

parser_t.add_argument("recipient_address", help="The public key of the wallet to send money to")
parser_t.add_argument("amount", help="The amount in Noobcash")

args = parser.parse_args()

if args.subcommand == "t":
    print("Transaction")
elif args.subcommand == "view":
    print("View")
elif args.subcommand == "balance":
    print("Balance")
elif args.subcommand == "help":
    print("Help")
