# Paste your version of blockchain.py from the client_mining_p
# folder here
import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        # One is here sine its not created like the rest of the hashes
        self.new_block(previous_hash='block_chain', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
           'index': len(self.chain) + 1,
           'timestamp': time(),
           'transaction': self.current_transactions,
           'proof': proof,
           'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the block to the chain
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]


    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        guess = f'{block_string}{proof}'.encode()
        #look at hash and convert into hexadecimal 
        guess_hash = hashlib.sha256(guess).hexdigest()
        # return True or False if has 3 leading zeros
        return guess_hash[:6] == "000000"

    def new_transactions(self, sender, recipient, amount):
 
        transaction = {'sender': sender,
                        'recipient': recipient,
                        'amount': amount
                }
        self.current_transactions.append(transaction)


        index = len(self.chain) + 1

        return index

# Instantiate our Node
app = Flask(__name__)
CORS(app)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()
print(blockchain.chain)
print(blockchain.hash(blockchain.last_block))


@app.route('/mine', methods=['POST'])
def mine():
    # Object in data - How flask works 
    data = request.get_json()

    if 'proof' not in data or 'id' not in data:
        response = {
            'message': 'missing a required property'
        }
        return jsonify(response), 400

    proof = data['proof']
    miner_id = data['id']

    block_string = json.dumps(blockchain.last_block, sort_keys=True)

    #Will return true or false
    #if proof is valid 
    if blockchain.valid_proof(block_string, proof):

        blockchain.new_transactions("0", miner_id, 1)

        # Forge the new Block by adding it to the chain with the proof
        previous_hash = blockchain.hash(blockchain.last_block)
        new_block = blockchain.new_block(proof,previous_hash)

        response = {
            'message': 'New Block Forged',

        }
        return jsonify(response), 200
    #else if proof is not valid 
    else: 
        response = {'message': 'proof is invalid or already submitted'}

        return jsonify(response), 200

@app.route('/tranactions/new', methods=['POST'])
def create_new_transaction():

    # retrieve the object in the data
    data = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in data for k in required):
        response = {'message': 'required properties not included'}

        return jsonify(response), 400
    sender = data['sender']
    recipient = data['recipient'] 
    amount = data['amount']  
    index = blockchain.new_transactions(sender, recipient, amount)

    response == {'message': f'added to block {index}'}

    return jsonify(response), 201



@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        'last_block': blockchain.last_block,
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
