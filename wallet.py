import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4



class Wallet:
    
    def __init__(self):
		##set

		#self.public_key
		#self.private_key
		#self_address
		#self.transactions
        key_object = RSA.generate(2048)
        self.public_key = key_object.publickey().export_key()
        self.private_key = key_object.export_key()
        self.balance = 0
        # print(self.public_key)
        # print(self.private_key)

    def balance():
        return balance
