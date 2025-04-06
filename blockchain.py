import hashlib
import json
import requests
from time import time
from hashlib import sha256
from urllib.parse import urlparse

class Blockchain(object):
    def __init__(self):
        self.chainLOO = []
        self.currentTransactionsLOO = []
        self.nodesLOO = set()

        self.new_block_loo(proof=100, previous_hash='Latyshev', nonce='15062002')

    def new_block_loo(self, proof, previous_hash=None, nonce=None):
        merkle_hash = self.merkle_root(self.currentTransactionsLOO)

        block = {
            'index': len(self.chainLOO) + 1,
            'timestamp': time(),
            'transactions': self.currentTransactionsLOO,
            'proof': proof,
            'previous_hash': previous_hash or self.hash_loo(self.chainLOO[-1]),
            'merkle_root': merkle_hash,
            'nonce': nonce
        }

        self.currentTransactionsLOO = []
        self.chainLOO.append(block)

        print(f"Хеш останнього блоку: {self.hash_loo(block)}")

        return block

    def register_node_loo(self, address):
        parsed_url = urlparse(address)
        self.nodesLOO.add(parsed_url.netloc)

    def new_transaction_loo(self, sender, recipient, amount):
        self.currentTransactionsLOO.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block_loo['index'] + 1

    @staticmethod
    def hash_loo(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block_loo(self):
        return self.chainLOO[-1]

    def proof_of_work_loo(self, last_proof):
        proof = 0
        while self.valid_proof_loo(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof_loo(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        print(f"Проба: {last_proof}, {proof} -> Хеш: {guess_hash}")
        return guess_hash.endswith("06")

    @staticmethod
    def merkle_root(transactions):
        if not transactions:
            return None

        hashes = [sha256(json.dumps(tx, sort_keys=True).encode()).hexdigest() for tx in transactions]

        while len(hashes) > 1:
            new_level = []
            for i in range(0, len(hashes), 2):
                if i + 1 < len(hashes):
                    new_level.append(sha256((hashes[i] + hashes[i + 1]).encode()).hexdigest())
                else:
                    new_level.append(hashes[i])
            hashes = new_level

        return hashes[0] if hashes else None

    def valid_chain_loo(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            if block['previous_hash'] != self.hash_loo(last_block):
                return False

            if not self.valid_proof_loo(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts_loo(self):
        neighbours = self.nodesLOO
        new_chain = None

        max_length = len(self.chainLOO)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain_loo(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chainLOO = new_chain
            return True

        return False


# blockchain = Blockchain()
#
# last_proof = blockchain.last_block_loo['proof']
# proof = blockchain.proof_of_work_loo(last_proof)
# blockchain.new_block_loo(proof)
#
# last_proof = blockchain.last_block_loo['proof']
# proof = blockchain.proof_of_work_loo(last_proof)
# blockchain.new_block_loo(proof)
#
# print("Blockchain:")
# print(json.dumps(blockchain.chainLOO, indent=4))

