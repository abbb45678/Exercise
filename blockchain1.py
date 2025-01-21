import hashlib
import time
import json


class Block:
    def __init__(self):
        self.chain = []
        self.current_transaction = []

        # 创建创世区块
        self.new_block(proof=100, pre_hash='0')

    def new_block(self, proof, pre_hash):
        # 创建新区块
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transaction': self.current_transaction,
            'proof': proof,
            'pre_hash': pre_hash or self.hash(self.chain[-1])  # 如果没有提供 pre_hash，则计算前一区块的哈希
        }

        # 清空当前交易记录
        self.current_transaction = []
        # 添加新块到链
        self.chain.append(block)

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


# 测试区块链
blockchain = Block()

# 新增一些交易
blockchain.new_transaction("Alice", "Bob", 50)
blockchain.new_transaction("Bob", "Charlie", 30)

# 找到一个有效的 proof
last_proof = blockchain.last_block['proof']
proof = blockchain.proof_of_work(last_proof)

# 创建新块
blockchain.new_block(proof=proof, pre_hash=blockchain.hash(blockchain.last_block))

# 打印区块链
for block in blockchain.chain:
    print(block)
