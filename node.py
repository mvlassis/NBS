#import block
import requests
from wallet import Wallet
import util

BOOTSTRAP_PORT = '5000'
BOOTSTRAP_IP = '192.168.1.18'

class Node:
    def __init__(self, is_bootstrap=False, nodes=5):
        self.NBC = 100
		##set

		#self.chain
		#self.current_id_count
		#self.NBCs
		#self.wallet
        self.nodes = nodes
        self.create_wallet()
        self.ring = []
        if is_bootstrap:
            self.id = 0
            self.ring.append([0, util.get_ip()+':'+BOOTSTRAP_PORT, self.wallet.public_key])
        else:
            self.id = self.register_request()
		#slef.ring[]   #here we store information for every node, as its id, its address (ip:port) its public key and its balance 

    def create_new_block():
        pass
        
	# Create a wallet for this node, with a public key and a private key
    def create_wallet(self):
        self.wallet = Wallet()

    def register_request(self):
        url = "http://"+BOOTSTRAP_IP+':'+BOOTSTRAP_PORT+"/register"
        body = {'ip_port': util.get_ip(), 'public_key' : self.wallet.public_key.decode('utf-8')}
        #print(url)
        response = requests.post(url, json=body)
        if response:
            self.id = response.json().get('id')
            print(self.id)
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs
    def register_node_to_ring(self, ip_port, public_key):
        self.ring.append([len(self.ring), ip_port, public_key])
        if len(self.ring)-1 == self.nodes:
            self.broadcast_ring()
        return len(self.ring)-1

    def broadcast_ring(self):
        body = [{"id": node[0], "ip_port": node[1], 'public_key': node[2].decode('utf-8')} for node in self.ring]
        print(body)
        for node in self.ring[1:]:
            ip_port = node[1]
            url = "http://"+ip_port+"/ring"
            body = {'ring' : body}
            response = requests.put(url, json=body)
            if response:
                print("Sucessful response")
                
    def add_to_ring(self, id, ip_port, public_key):
        self.ring.append([id, ip_port, public_key])
    
    def print_ring(self):
        print(self.ring)

    def create_transaction(sender, receiver, signature):
		#remember to broadcast it
        pass


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


