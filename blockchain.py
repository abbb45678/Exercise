import hashlib


class Proofofwork():
    def __init__(self, block):
        self.block = block

    def mine(self):
        i = 0
        prefix = '0000'

        while True:
            nonce = str(i)
            message = hashlib.sha256()
            message.update(str(self.block.data).encode('utf-8'))
            message.update(nonce.encode('utf-8'))
            digest = message.hexdigest()
            if digest.startswith(prefix):
                return nonce, digest
            i += 1


class Block:
    def __init__(self, data, pre_hash):
        self.pre_hash = pre_hash
        self.data = data
        self.nonce = ""

    def hash(self):
        message = hashlib.sha256()
        message.update(str(self.data).encode('utf-8'))
        message.update(str(self.nonce).encode('utf-8'))
        digest = message.hexdigest()
        return digest


def create_first_block():
    block = Block(data="First Block", pre_hash="")
    pow = Proofofwork(block)
    nonce, digest = pow.mine()
    block.nonce = nonce
    return block


class BlockChain:
    def __init__(self):
        self.blocks = [create_first_block()]

    def add_block(self, n):
        global new_block
        m = 0
        while m < n:
            data = input(f"请输入你要添加的第{m + 1}个区块的数据：")
            pre_block = self.blocks[len(self.blocks) - 1]
            new_block = Block(data, pre_block.hash)
            pow = Proofofwork(new_block)
            nonce, digest = pow.mine()
            new_block.nonce = nonce
            self.blocks.append(new_block)
            m += 1
        return new_block


bc = BlockChain()
n = eval(input("请输入你要添加的区块数量："))
bc.add_block(n)
print("\n")
print("区块链的各个区块信息如下：")
for i in bc.blocks:
    print(f"前一个区块的哈希值：{i.pre_hash}")
    print(f"当前区块的数据：{i.data}")
    print(f"当前区块的哈希值：{i.hash}")
    print("\n")
