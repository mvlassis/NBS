# NBS
NBS is a simple blockchain system that facilitates transactions of an imaginary coin named Noobcoin (NBC), with consensus reached via proof-of-work. This project was created as part of the 2022-2023 course in Distributed Systems from the National Technical University of Athens (NTUA).

## Design
The source code follows object-oriented design and is based around the following classes:
- Node: Represents a computer node that has its own wallet and can make transactions with other nodes.
- Blockchain: A ledger where all transactions are validated and stored. Each node has a copy of the blockchain and can add new blocks it it. Blocks are added after the node has successfully mined for a new block, or after receiving a valid block from another node.
- Block: A series of transactions grouped together. Each block can store up to a certain number of transactions, specified by the MINING_CAPACITY constant. For a block to be valid, its SHA256 hash must begin from a certain number of 0s. specified by the MINING_DIFFICULTY constant.
- Transaction: Represents a single transaction. Each transaction **must** have a sender address, a recipient address, the amount to send, and a list of valid **transaction inputs** and **transaction outputs**.
- Wallet: Represents the wallet of a node. Each wallet is represented by its RSA-2048 public key, and can sign transactions using its RSA-2048 private key. Other nodes that receive the transaction have to validate the signature using the public key of the sender.

### Network
To initialize the blockchain system, a bootstrap node must be created. The bootstrap node has a record (named the "ring") of the IP&port and the public keys of all participating nodes in the network.

To connect to the Noobcash network, a node has to communicate with the bootstrap node and receive its unique ID. After all nodes have been registered, the bootstrap node sends the ring to all participating nodes, and then transactions can occur.

### CLI
Users can interact with the system using a basic command-line interface in cli.py. The CLI utilized the *argparse* module and can perform the following functions:
- t <address> <amount>: Send <amount> of NBCs to the specified IP&Port.
- balance: Print the current balance of your wallet.
- view: Print the last validated block in the blockchain
- help: Print helpful information about how to use the CLI.

Communication between nodes or between the CLI and the respective node is done using the REST API in rest.py. A node can start in bootstrap mode with the "-b" flag and specify the number of participating nodes with the "-n" options. For example, the bootstrap node can be initialized with 5 participating nodes by running:
```
python rest.py -b -n 5
```
All other nodes have to run:
```
python rest.py 
```

## Language & Libraries
The whole project uses the Python programming language. Apart from the standard Python libraries, the code also uses the following Python modules:
- flash 
- flask_cors
- requests
- pycryptodome
- argparse

