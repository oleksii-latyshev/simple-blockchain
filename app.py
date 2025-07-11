import sys
import argparse
from uuid import uuid4
from blockchain import Blockchain
from flask import Flask, jsonify, request

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block_loo
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work_loo(last_proof)

    blockchain.new_transaction_loo(
        sender="0",
        recipient=node_identifier,
        amount=15,
    )

    previous_hash = blockchain.hash_loo(last_block)
    block = blockchain.new_block_loo(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'merkle_root': block['merkle_root']
    }

    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction_loo(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chainLOO,
        'length': len(blockchain.chainLOO),
    }

    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node_loo(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodesLOO),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts_loo()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chainLOO
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chainLOO
        }

    return jsonify(response), 200



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=5000, type=int, help='Port to run the server on')
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port)