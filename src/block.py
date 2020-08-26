import json
from hashlib import sha256

class Block:
    # block class
    def __init__(self,index id, previous_hash,vote,nonce=0):
        #initialise block note create genisis node creation
        # thought of using index for difficulty but ?
        #edit dont use index for difficulty and it isnt a requirement
        #for our systema hacker could potentaly modify every index making difficulty low so stick t position in array
        self.id = id 
        self.vote = vote
        self.previous_hash = previous_hash
        self.nonce= nonce
        

    def print_block(self,proof):
        print("hash: " + str(proof))
        print("id:"+ str(self.id))
        print("prev_hash:"+ str(self.previous_hash))
        print("vote"+ str(self.vote)) 
        print("nonce: "+str(self.nonce))
        




    def compute_hash(self):
        # re work instead of hash check for id in stopping revoting should still work and less complexity
        block_string = json.dumps(self.__dict__, sort_keys=True)
        #for debuging remove later
        print(sha256(block_string.encode()).hexdigest())
        return sha256(block_string.encode()).hexdigest()

#test if hash remains consistent works
#r1=Block(342434,34234,'trevt')
#r1.compute_hash()
          
# instead of arry might want to store chain in form of dictionary with keys 
#as id for quick look up and for duplicates in revoting

class Blockchain():
    """blockchain class"""
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    def create_genesis_block(self):
        genesis_block = Block(0, 0,0)
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
        
    @property
    def last_block(self):
        return self.chain[-1]


    difficulty =2

    def proof_of_work(self, block):
        # the one who creates the block will have to find the right nounce value for each difficulty 
        #and complexity increases as dificulty increases
        block.nonce=0
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
    #in p2p network should i instead of verifying this vay verify by comparison to other nodes?
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    #test func to print blocks
    def print_blocks(self):
        for blocks in self.chain:
            print("hash: "+str(blocks.hash))
            print("id:"+ str(blocks.id))
            print("prev_hash:"+ str(blocks.previous_hash))
            print("vote"+ str(blocks.vote))
            print("nonce"+ str(blocks.nonce))


#test 1 
#for if genisis block is created works
print("test 1 ")
chain = Blockchain()
chain.print_blocks()

#test 2 
#for if proof of work gets calculated
print("test 2 ")
block1 = Block(353424, chain.last_block.hash,"Me")
proof_block1= chain.proof_of_work(block1)
print( "proof: "+ str(proof_block1))

#test 3
# for if nounce is updated
print("test 3 ")
block1.print_block( proof_block1)

#test 4 
# if block is valid add to cahin
#when sending block to other nodes always send precalculated hash so we can check if node has been tampered with
print ("test 4")
if(chain.is_valid_proof(block1, proof_block1)):
    print("valid")

#test 5
#add block to chain and verify
print ("test 5")
chain.add_block(block1,proof_block1)
chain.print_blocks()