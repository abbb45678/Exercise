from flask import Flask
from flask import request
import json
import requests
import hashlib as hasher
import datetime as date
from colorama import Fore
import pickle

node = Flask(__name__)





# 定义区块结构体
class Block:

    # 初始化函数
    def __init__(self, index, timestamp, date, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.date = date
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    # 哈希算法实现
    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('UTF-8')
                   + str(self.timestamp).encode('UTF-8')
                   + str(self.date).encode('UTF-8')
                   + str(self.previous_hash).encode('UTF-8'))
        return sha.hexdigest()


class Blockchain:
    def __init__(self):
        self.blockchain = []

    # 生成创世块


def create_genesis_block(self):
    return Block(0, date.datetime.now(), {
        "proof-of-work": 9,
        "transactions": None
    }, "0")


# 配置信息和变量定义
# 本矿工的ip
my_node = input()
miner_address = "kuanggong_win"

# 所有矿工的ip
node1 = ""
node2 = ""
all_nodes = {node1, node2}
peer_nodes = all_nodes.difference({my_node})
mining = True
timeout = 2  # 设置超时时间为2s

# 区块链
bc = Blockchain()
bc.blockchain.append(create_genesis_block())

# 该节点待处理的交易
this_nodes_transactions = []


# 处理post请求，处理区块的交易
@node.route('/txion', methods=['POST'])
def transaction():
    new_txion = request.get_json()  # 提取交易数据
    this_nodes_transactions.append(new_txion)  # 添加交易到待处理列表中

    # 显示交易信息
    print("New transaction")
    print("FROM: {}".format(new_txion['from'].encode('ascii', 'replace')))
    print("TO:{}".format(new_txion['to'].encode('ascii', 'replace')))
    print("AMOUNT:{}\n".format(new_txion['amount']))

    # 回应客户端交易已提交
    return "Transaction submission successful\n"


# 处理GET请求，返回区块链的信息
@node.route('/txion', methods=['GET'])
def get_block():
    # 处理成json格式
    blocks = []
    for block in bc.blockchain:
        blocks.append({
            "index": block.date,
            "timestamp": str(block.timestamp),
            "date": block.date,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })
        chain_to_send = json.dumps(blocks, indent=2)
        chain_to_send_object = pickle.dumps(bc.blockchain)
        return chain_to_send_object

    #获取其他节点的数据
def find_new_chains():
     #用GET请求每个节点的区块链
    other_chains = []
    for node_url in peer_nodes:
        try:
            block =requests.get(node_url +"/blocks",timeout=timeout)
            block = pickle.loads(block.content) #将JSON格式转成python字典
            other_chains.append(block)
            print('已拿到其他矿工账本')
        except:
            print('没有找到其他矿工')
            pass
    return other_chains

#工作量证明算法
def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 9 == 0 and incrementor % last_proof ==0):
        incrementor += 1
    return incrementor

#处理GET请求
@node.route('/mine',methods=['GET'])
def mine():
    # 获取上一个块的proot of work
    last_block = bc.blockchain[len(bc.blockchain)-1]
    last_proof = last_block.date['proof-of-work']

    proof = proof_of_work(last_proof)

    this_nodes_transactions.append(
        {"from":"network", "to":miner_address,"amount":1}
    )

    new_block_date = {
        "proof-of-work":proof,
        "transactions":list(this_nodes_transactions)
    }
    new_block_index = last_block.index +1
    new_block_timestamp = this_timestamp =date.datetime.now()
    last_block_hash = last_block.hash

    #清空待处理交易列表
    this_nodes_transactions[:] =[]

    #创建新块
    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_date,
        last_block_hash
    )
    print("挖到一个币")

    #共识算法
    other_chains = find_new_chains()
    longest_chain = bc.blockchain
    for chain in other_chains:
        print("别人的账本长度：",len(chain))
        if len(longest_chain)<len(chain):
            print("自己的账本不如别人的长")
            longest_chain= chain
    if len(bc.blockchain)==len(longest_chain):
        bc.blockchain.append(mined_block)
    else:
        bc.blockchain = longest_chain
    print("共识算法后自己的账本长度：",len(bc.blockchain))
    return "okokok\n"

if __name__=='__main__':
    node.run('0.0.0.0',5000)


