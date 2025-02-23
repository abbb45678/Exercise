import hashlib
import json
import time
import os.path


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.tx_id = hashlib.sha256(f"{sender}{receiver}{amount}{time.time()}".encode()).hexdigest()

    def to_dict(self):
        return {"tx_id": self.tx_id, "sender": self.sender, "receiver": self.receiver, "amount": self.amount}

    def __repr__(self):
        return f"Transaction(sender={self.sender},receiver={self.receiver},amount={self.amount},tx_id={self.tx_id})"


class Block:
    def __init__(self, index, pre_hash, timestamp, transactions, nonce=0):
        self.index = index
        self.pre_hash = pre_hash
        self.timestamp = timestamp
        self.transactions = [
            tx if isinstance(tx, Transaction)
            else Transaction(
                tx["sender"],
                tx["receiver"],
                tx["amount"],
                tx_id=tx["tx_id"]
            )
            for tx in transactions
        ]
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
    genesis_tx = Transaction(None, "system_wallet", 10000)
    return Block(0, "0", time.time(), [genesis_tx])


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
            with open("transaction.json", "r") as f:
                chain_data = json.load(f)
                self.chain = []
                for block_data in chain_data:
                    # 将字典转为 Transaction 对象
                    transactions = [
                        Transaction(tx["sender"], tx["receiver"], tx["amount"])
                        for tx in block_data["transactions"]
                    ]

                    block = Block(
                        index=block_data["index"],
                        pre_hash=block_data["pre_hash"],
                        timestamp=block_data["timestamp"],
                        transactions=transactions,
                        nonce=block_data["nonce"]
                    )
                    block.hash = block_data["hash"]  # 直接赋哈希值避免重复计算
                    self.chain.append(block)

    def get_last_block(self):
        return self.chain[-1]

    def get_balance(self, address):
        balance = 0
        # 计算区块链中已确认的交易
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.receiver == address:
                    balance += tx.amount
        # 计算当前交易池中的未确认交易
        for tx in self.current_transactions:
            if tx.sender == address:
                balance -= tx.amount
            if tx.receiver == address:
                balance += tx.amount
        return balance

    def valid_transaction(self, transaction):
        if transaction.sender is None:
            return True  # 系统交易直接通过
        sender_balance = self.get_balance(transaction.sender)  # 包括当前交易池中的交易
        return sender_balance >= transaction.amount

    def create_transactions(self, transaction):
        existing_ids = {tx.tx_id for tx in self.current_transactions}
        if transaction.tx_id in existing_ids:
            print("交易已存在！")
            return
        if self.valid_transaction(transaction):
            self.current_transactions.append(transaction)
            self.save_chain()
        else:
            print("交易无效！")

    def mine_current_transactions(self, address_reward):
        reward_tx = Transaction(None, address_reward, self.mining_reward)
        self.current_transactions.insert(0, reward_tx)

        new_block = Block(len(self.chain), self.get_last_block().hash, time.time(), self.current_transactions)
        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)
        self.save_chain()

        self.current_transactions = []

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
    blockchain = Blockchain()

    # 验证创世区块中 system_wallet 余额
    print("system_wallet 初始余额:", blockchain.get_balance("system_wallet"))

    # 创建有效交易：系统向user1 转账 500
    tx1 = Transaction("system_wallet", "user1", 500)
    blockchain.create_transactions(tx1)

    # 创建有效交易：user1向ww 转账 200
    tx2 = Transaction("user1", "ww", 200)
    blockchain.create_transactions(tx2)

    # 挖矿确认交易
    print("开始挖矿...")
    blockchain.mine_current_transactions("矿工1")
    print("挖矿后区块链的状态：")
    print(blockchain)

    # 打印余额
    print("system_wallet 余额:", blockchain.get_balance("system_wallet"))
    print("user1 余额:", blockchain.get_balance("user1"))
    print("ww 余额:", blockchain.get_balance("ww"))
    print("矿工1 余额:", blockchain.get_balance("矿工1"))
