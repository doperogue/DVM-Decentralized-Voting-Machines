import block as bl


# create genesis block 
chain = bl.Blockchain()


# create block based on input from user after verification
class vote:
    def __init__(self, id,vote):
        #initialise block note create genisis node creation
        self.id = id 
        self.vote= vote
        self.vote_block = bl.Block(id,chain.last_block.hash,vote)
    #def checkvote(self)
        #function to check if vote exist in chain
        #use dictionry 

    def submit_vote(self)
        proof = bl.proof_of_work(chain,vote_block)
        


    
 
        
        



# verify block and check duplicates and send to other nodes in p2p network