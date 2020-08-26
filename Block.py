import json
from hashlib import sha256

class Block:
    # block class
    def __init__(self, id,previous_hash):
        #initialise block note create genisis node creation
        self.id = id 
        self.previous_hash = previous_hash
        self.vote= vote
        self.previous_hash = previous_hash



    def compute_hash(self):
        # to compute hash may or may not need more complexity make sure not to add self.vote 
        #to hash calculation so vote does not determine the hash may add dob or other static values to calculate hash
        block_string = json.dumps(self.id, sort_keys=True)
        print(sha256(block_string.encode()).hexdigest())
        return sha256(block_string.encode()).hexdigest()

#test if hash remains consistent works
#r1=Block(342434)
#r1.compute_hash()


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

# implement proof ogf work will do later today yogi wants to play dota
