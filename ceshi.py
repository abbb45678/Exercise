import hashlib


class Proofofwork:
    def __init__(self, block):
        self.block = block

    def mine(self):
        i = 0
        prefix = '0000'  # 设置工作量证明的目标前缀

        while True:
            nonce = str(i)
            message = hashlib.sha256()
            # 在哈希计算中同时考虑区块的数据和 nonce
            message.update(str(self.block.data).encode('utf-8'))
            message.update(nonce.encode('utf-8'))  # nonce 应该加入哈希计算
            digest = message.hexdigest()
            if digest.startswith(prefix):  # 如果哈希值以 0000 开头，说明成功找到 nonce
                return nonce, digest
            i += 1


class Block:
    def __init__(self, data, pre_hash):
        self.pre_hash = pre_hash
        self.data = data
        self.nonce = ""  # 初始 nonce 为空

    def hash(self):
        # 在计算区块哈希时，同时考虑 data 和 nonce
        message = hashlib.sha256()
        message.update(str(self.data).encode('utf-8'))
        message.update(str(self.nonce).encode('utf-8'))  # 计算时需要包含 nonce
        digest = message.hexdigest()
        return digest


def create_first_block():
    block = Block(data="First Block", pre_hash="")  # 创世区块没有前一个哈希
    pow = Proofofwork(block)
    nonce, digest = pow.mine()  # 挖矿过程找到 nonce
    block.nonce = nonce  # 将找到的 nonce 存储到区块中
    return block


class BlockChain:
    def __init__(self):
        self.blocks = [create_first_block()]  # 初始区块链包含创世区块

    def add_block(self, n):
        global new_block
        m = 0
        while m < n:
            data = input(f"请输入你要添加的第{m + 1}个区块的数据：")
            pre_block = self.blocks[len(self.blocks) - 1]  # 获取上一个区块
            new_block = Block(data, pre_block.hash())  # 新区块的 pre_hash 是前一个区块的哈希
            pow = Proofofwork(new_block)
            nonce, digest = pow.mine()  # 挖矿过程找到 nonce
            new_block.nonce = nonce  # 将 nonce 存储到新区块中
            self.blocks.append(new_block)  # 将新区块加入区块链
            m += 1
        return new_block


# 主程序
bc = BlockChain()
n = int(input("请输入你要添加的区块数量："))
bc.add_block(n)  # 添加指定数量的区块

print("\n区块链的各个区块信息如下：")
for i in bc.blocks:
    print(f"前一个区块的哈希值：{i.pre_hash}")
    print(f"当前区块的数据：{i.data}")
    print(f"当前区块的哈希值：{i.hash()}")
    print("\n")
