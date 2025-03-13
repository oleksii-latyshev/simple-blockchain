from uuid import uuid4
from blockchain import Blockchain
from flask import Flask, jsonify, request

# Створюємо екземпляр вузла
app = Flask(__name__)

# Генеруємо унікальну на глобальному рівні адресу для цього вузла
node_identifier = str(uuid4()).replace('-', '')

# Створюємо екземпляр блокчейну
blockchain = Blockchain()

#Створення кінцевої точки /mine, яка є GET-запитом
@app.route('/mine', methods=['GET'])
def mine():
    # Запускаємо алгоритм підтвердження роботи, щоб отримати наступний пруф
    last_block = blockchain.last_block_loo
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work_loo(last_proof)

    # Повинні отримати винагороду за знайдене підтвердження
    # Відправник "0" означає, що вузол заробив коін
    blockchain.new_transaction_loo(
    sender="0",
    recipient=node_identifier,
    amount=1,
    )

    # Створюємо новий блок, шляхом внесення його в ланцюг
    previous_hash = blockchain.hash_loo(last_block)
    block = blockchain.new_block_loo(proof, previous_hash)
    response = {
    'message': "New Block Forged",
    'index': block['index'],
    'transactions': block['transactions'],
    'proof': block['proof'],
    'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

# Створення кінцевої точки /transactions/new, яка є POST-запитом, так як будемо відправляти туди дані;
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Перевірка того, що необхідні поля знаходяться серед POST-даних
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Створення нової транзакції
    index = blockchain.new_transaction_loo(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

# Створення кінцевої точки /chain, яка повертає весь блокчейн;
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chainLOO,
        'length': len(blockchain.chainLOO),
    }

    return jsonify(response), 200

# Запускає сервер на порт: 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)