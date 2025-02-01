import hashlib
import json
import time
import os.path


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_dict(self):
        return {"sender": self.sender, "receiver": self.receiver, "amount": self.amount}

    def __repr__(self):
        return f"Transaction(sender={self.sender},receiver={self.receiver},amount={self.amount})"


class Block:
    def __init__(self, index, pre_hash, timestamp, transactions, nonce=0):
        self.index = index
        self.pre_hash = pre_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        Block_date = {
            "index": self.index,
            "pre_hash": self.pre_hash,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "nonce": self.nonce
        }
        block_string = json.dumps(Block_date, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        self.timestamp = time.time()
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"挖矿成功，区块的哈希值为：{self.hash}")

    def __repr__(self):
        return f"区块:[index={self.index},pre_hash={self.pre_hash}, hash={self.hash},timestamp={self.timestamp},transactions={self.transactions},nonce={self.nonce}]"


def create_genesis_block():
    return Block(0, "0", time.time(), [])


class Blockchain:
    def __init__(self):
        self.chain = [create_genesis_block()]
        self.current_transactions = []
        self.difficulty = 4
        self.mining_reward = 100
        self.load_chain()

    def save_chain(self):
        with open("transaction.json", "w") as f:
            chain_date = [block.__dict__ for block in self.chain]
            json.dump(chain_date, f, default=lambda x: x.__dict__, indent=4)

    def load_chain(self):
        if os.path.exists("transaction.json"):
            with open("transaction.json", "w") as f:
                chain_date = json.load(f)
                self.chain = [Block(**date) for date in chain_date]

    def get_last_block(self):
        return self.chain[-1]

    def get_balance(self, address):
        balance = 1000
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.receiver == address:
                    balance += tx.amount
        return balance

    def valid_transaction(self, transaction):
        sender_balance = self.get_balance(transaction.sender)
        return sender_balance >= transaction.amount

    def create_transactions(self, transaction):
        if self.valid_transaction(transaction):
            self.current_transactions.append(transaction)
            self.save_chain()
        else:
            print("交易无效！")

    def mine_current_transactions(self, address_reward):
        new_block = Block(len(self.chain), self.get_last_block().hash, time.time(), self.current_transactions)
        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)
        self.save_chain()

        self.current_transactions = [
            Transaction(None, address_reward, self.mining_reward)
        ]

    def is_valid_block(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            pre_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                print("当前区块哈希值无效！")
                return False
            if pre_block.hash != pre_block.calculate_hash():
                print("前一个区块的哈希值无效！")
                return False

        return True

    def __repr__(self):
        return f"\n".join(str(block) for block in self.chain)


if __name__ == "__main__":
    blockchain=Blockchain()

    blockchain.create_transactions(Transaction("杜牧","李清照",70))
    print("开始挖矿...")
    blockchain.mine_current_transactions("矿工3")
    print("挖矿后的区块链的状态：")
    print(blockchain)

    print("区块链是否有效？",blockchain.is_valid_block())
