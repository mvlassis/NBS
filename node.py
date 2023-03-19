import block
import requests
from wallet import Wallet
from threading import Thread
import time
import util

BOOTSTRAP_PORT = '5000'
BOOTSTRAP_IP = '192.168.0.4'

class Node:
    def __init__(self, is_bootstrap=False, nodes=5):
        self.NBC = 100
		##set

		#self.chain
		#self.current_id_count
		#self.NBCs
		#self.wallet
        self.nodes = nodes
        self.sender_address = util.get_ip()+':'+BOOTSTRAP_PORT
        self.create_wallet()
        self.unspent_transactions = []
        self.ring = []
        if is_bootstrap:
            print("Bootstrap node created, nodes = ", self.nodes)
            self.id = 0
            self.ring.append([0, util.get_ip()+':'+BOOTSTRAP_PORT, self.wallet.public_key])
		#slef.ring[]   #here we store information for every node, as its id, its address (ip:port) its public key and its balance 

    def create_new_block():
        pass
        
	# Create a wallet for this node, with a public key and a private key
    def create_wallet(self):
        self.wallet = Wallet()

    def register_request(self):
        url = "http://"+BOOTSTRAP_IP+':'+BOOTSTRAP_PORT+"/register"
        body = {'ip_port': util.get_ip()+":"+BOOTSTRAP_PORT, 'public_key' : self.wallet.public_key.decode('utf-8')}
        #print(url)
        response = requests.post(url, json=body)
        if response:
            self.id = response.json().get('id')
            print("Registered successfully, id = ", self.id)
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs
    def register_node_to_ring(self, ip_port, public_key):
        self.ring.append([len(self.ring), ip_port, public_key])
        if len(self.ring) == self.nodes:
            thread = Thread(target=self.broadcast_ring)
            thread.start()
        return len(self.ring)-1

    def broadcast_ring(self):
        time.sleep(5)
        body = [{"id": node[0], "ip_port": node[1], 'public_key': node[2].decode('utf-8')} for node in self.ring]
        print("ABOUT TO BROADCAST RING")
        for node in self.ring[1:]:
            ip_port = node[1]
            # url = "http://"+BOOTSTRAP_IP+':'+BOOTSTRAP_PORT+"/register"
            url = "http://"+ip_port+"/ring"
            body = {'ring' : body}
            response = requests.put(url, json=body)
            if response:
                print("Successful response")
                
    def add_to_ring(self, id, ip_port, public_key):
        self.ring.append([id, ip_port, public_key])
    
    def print_ring(self):
        print(self.ring)

    def create_transaction(self, receiver_address, amount):
        # Remember to broadcast it
        cur_sum = 0
        remaining = 0
        index = -1
        transaction_inputs = []
        for i, unspent_transaction in enumerate(self.unspent_transactions):
            cur_sum += unspent_transaction['amount']
            transaction_inputs.append(unspent_transaction['id'])
            if cur_sum >= amount:
                remaining = cur_sum - amount
                index = i
                break
        if t_sum < amount:
            print("Not enough UTXOs in your wallet")
            return               

        transaction = Transaction(self.sender_address, self.wallet.private_key,
                                  receiver_address, transaction_inputs,
                                  transaction_outputs, amount)
        
        transaction_outputs = []
        d1 = dict()
        d1['id'] = transaction.transaction_id
        d1['target'] = receiver_address
        d1['amount'] = amount

        d2 = dict()
        d1['id'] = transaction.transaction_id
        d2['target'] = self.sender_address
        d2['amount'] = remaining
        transaction_outputs.append(d1)
        transaction_outputs.append(d2)
        
        transaction.transaction_outputs = transaction_outputs

        if index == len(self.unspent_transactions) - 1:
            self.unspent_transactions = [transaction_outputs[1]]
        else:
            self.unspent_transactions[index+1:]
            self.unspent_transactions.append[transactions_outputs[1]]

        all_utxos[self.sender_address] = self.unspent_transactions.copy()
        all_utxos[receiver_address].append(transaction_outputs[0])

        transaction.sign_transaction()

        self.broadcast_transaction()
        
        self.add_transaction_to_block()
        


    def broadcast_transaction():
        pass


    def validate_transaction():
		#use of signature and NBCs balance
        pass

    def add_transaction_to_block():
		#if enough transactions  mine
        pass


    def mine_block():
        pass


    def broadcast_block():
        pass
		

#    def valid_proof(.., difficulty=MINING_DIFFICULTY):


	# Consensus functions

    def valid_chain(self, chain):
		#check for the longer chain accroose all nodes
        pass

    def resolve_conflicts(self):
		#resolve correct chain
        pass


