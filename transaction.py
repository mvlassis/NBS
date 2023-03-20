from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import json

import requests
from flask import Flask, jsonify, request, render_template


class Transaction:

	def __init__(self, sender_address, recipient_address, amount,
				 transaction_inputs, transaction_outputs=[]):
		##set

		#self.sender_address: To public key του wallet από το οποίο προέρχονται τα χρήματα
		self.sender_address = sender_address

		#self.receiver_address: To public key του wallet στο οποίο θα καταλήξουν τα χρήματα
		self.recipient_address = recipient_address
		
		#self.amount: το ποσό που θα μεταφερθεί
		self.amount = amount

		#self.transaction_inputs: λίστα από Transaction Input
		self.transaction_inputs = transaction_inputs
		
		#self.transaction_outputs: λίστα από Transaction Output = []
		self.transaction_outputs = transaction_outputs
		#selfSignature    
		
		#self.transaction_id: το hash του transaction
		self.transaction_id = SHA256.new(self.to_json().encode()).hexdigest()

	def __str__(self):
		string = "TRANSACTION: " + self.transaction_id + '\n'
		string += "Sender:    " + self.sender_address + '\n'
		string += "Recipient: " + self.recipient_address + '\n'
		string += "Amount:    " + str(self.amount) + '\n'
		return string
	
	def to_json(self):
		transactions = {'sender_address' : self.sender_address,
                        'recipient_address' : self.recipient_address,
						'amount' : self.amount,
                        'transaction_inputs' : self.transaction_inputs,
                        'transaction_outputs' : self.transaction_outputs,
        }
		return json.dumps(transactions)

	def sign_transaction(self, private_key):
		"""
		Sign transaction with private key
		"""
		
		transaction_bytes = self.to_json().encode()
		hash_object = SHA256.new(transaction_bytes)
		key = RSA.importKey(private_key)
		signature = PKCS1_v1_5.new(key).sign(hash_object)
		return signature

# key_object = RSA.generate(2048)
# public_key = key_object.publickey().export_key()
# private_key = key_object.export_key()
# trans = Transaction('192.168.0.5:5000', private_key, '192.168.0.4:5000', '10')
# trans.sign_transaction()
