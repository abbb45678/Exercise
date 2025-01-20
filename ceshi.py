import hashlib


class prooffwork():
    def __init__(self, block):
        self.block = block

    def mine(self):
        i = 0
        prexit = '0000'

        while True:
            nonce = str(i)
            message = hashlib.sha256()
            message.update(str(self.block.data).encode('utf-8'))
            message.update(nonce.encode('utf-8'))
            digest = message.hexdigest()
            if digest.startswith(prexit):
                return nonce, digest
            i += 1


class Block:
    def __init__(self, data, pre_hash):
        self.data = data
        self.pre_hash = pre_hash
        self.nonce = ""

    def hash(self):
        message = hashlib.sha256()
        message.update(str(self.data).encode('utf-8'))
        message.update(str(self.nonce).encode('utf-8'))
        digest = message.hexdigest()
        return digest


def create_first_block():
    data = input("请输入创世块的数据信息：")
    block = Block(data=data, pre_hash="")
    pow = prooffwork(block)
    nonce, digest = pow.mine()
    block.nonce = nonce
    return block


class BlockChain:
    def __init__(self):
        self.blocks = [create_first_block()]

    def add_newblock(self, n):
        global new_Block
        m = 0
        while m < n:
            data = input(f"请输入你要添加的第{m + 1}个区块的数据：")
            pre_block = self.blocks[len(self.blocks) - 1]
            new_Block = Block(data, pre_block.hash)
            pow = prooffwork(new_Block)
            nonce, digest = pow.mine()
            new_Block.nonce = nonce
            self.blocks.append(new_Block)
            m += 1
        return new_Block


if __name__ == "__main__":
    bc = BlockChain()
    n = int(input("请输入你要添加的区块的数量："))
    bc.add_newblock(n)
    print("区块链的各个区块信息如下：")
    print("\n")
    for block in bc.blocks:
        print(f"前一个区块的哈希：{block.pre_hash}")
        print(f"当前区块的数据：{block.data}")
        print(f"当前区块的哈希：{block.hash()}")
        print()