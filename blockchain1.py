import hashlib
import time
import json
from uuid import uuid4

from flask import jsonify, Flask, request


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transaction = []

        # 创建创世区块
        self.new_block(proof=100, pre_hash='0')

    def new_block(self, proof, pre_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transaction,
            'proof': proof,
            'pre_hash': pre_hash or self.hash(self.chain[-1])  # 如果没有提供 pre_hash，则计算前一区块的哈希
        }
        self.current_transaction = []
        self.chain.append(block)
        return block  # 确保返回新创建的区块

    def new_transaction(self, sender, recipient, amount):
        # 添加新的交易到当前交易列表
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.current_transaction.append(transaction)

        # 返回新的区块的索引
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # 计算区块的哈希
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # 返回链上的最后一个区块
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        # 工作量证明，寻找符合条件的 proof
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        # 检查 proof 是否满足要求
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # 需要前两位为 0
        return guess_hash[:2] == "00"


app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()


@app.route('/')
def home():
    return "Welcome to the Blockchain! Visit /mine, /transactions/new, or /chain for more information."


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_transaction(sender="0", recipient=node_identifier, amount=1)
    block = blockchain.new_block(proof, pre_hash=blockchain.hash(last_block))  # 确保传递 pre_hash 参数
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'pre_hash': block['pre_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
