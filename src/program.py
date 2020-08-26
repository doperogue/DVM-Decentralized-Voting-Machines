import block as bl
###Ooooo add a current vote tally record and and voting on who is cooler lol 

# create genesis block 
vote_chain = bl.Blockchain()

class vote():
    def __init__(self,id,candidate):
        self.id = id
        self.candidate = candidate
        
#test vote
vote_made = vote(342431, "Me again lol")

def create_vote_block(vote)
    #called to create a vote block
    vote_block =  bl.Block(vote.id,vote_chain.last_block.hash,vote.candidate) 
    return vote_block

def submit_vote()
    #called when vote starts processing
    # stat calculating hash with proof_of _work
    vote_made_block = create_vote_block(vote_made)
    proof_vote_block = vote_chain.proof_of_work(vote_made_block)
    vote_chain.add_block(vote_made_block, proof_vote_block)

#create a function to send block to different members of p2p network




    
#following code to be run if submit is pressed
        
        



# verify block and check duplicates and send to other nodes in p2p network