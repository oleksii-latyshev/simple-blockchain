import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chainLOO = []
        self.currentTransactionsLOO = []

        self.new_block_loo(proof=100, previous_hash='Latyshev', nonce='15062002')

    def new_block_loo(self, proof, previous_hash=None, nonce=None):

        block = {
            'index': len(self.chainLOO) + 1,
            'timestamp': time(),
            'transactions': self.currentTransactionsLOO,
            'proof': proof,
            'previous_hash': previous_hash or self.hash_loo(self.chainLOO[-1]),
            'nonce': nonce
        }

        self.currentTransactionsLOO = []
        self.chainLOO.append(block)

        print(f"Хеш останнього блоку: {self.hash_loo(block)}")

        return block

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

