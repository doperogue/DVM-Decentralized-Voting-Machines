import json
from hashlib import sha256

class Block:
    # block class
    def __init__(self, id, previous_hash,vote,nounce=0):
        #initialise block note create genisis node creation
        self.id = id 
        self.vote= vote
        self.previous_hash = previous_hash
        self.nounce= nounce




    def compute_hash(self):
        # re work instead of hash check for id in stopping revoting should still work and less complexity
        block_string = json.dumps(self.__dict__, sort_keys=True)
        print(sha256(block_string.encode()).hexdigest())
        return sha256(block_string.encode()).hexdigest()

#test if hash remains consistent works
#r1=Block(342434,34234,'trevt')
#r1.compute_hash()


# instead of arry might want to store chain in form of dictionary with keys as id for quick look up and for duplicates in revoting

class Blockchain():
    """blockchain class"""
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    def create_genesis_block(self,id):
        genesis_block = Block(id, 0)
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
        
    @property
    def last_block(self):
        return self.chain[-1]


    difficulty =2

    def proof_of_work(self, block):
        # the one who creates the block will have to find the right nounce value for each difficulty 
        #and complexity increases as dificulty increases
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    def add_block(self, block, proof):
        #block is added in each node in p2p with proof provied by initial block creatoror miner and checked if it is valid
        #if so hash is updated with proff ie starting 0000bits and  stored
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True
 
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())



