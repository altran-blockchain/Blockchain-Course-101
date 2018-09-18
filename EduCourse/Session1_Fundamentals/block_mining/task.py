# Lets do some mining
# Import SimpleBlock that we created earlier and
# lets extend it
from Session1_Fundamentals.block_basics.task import SimpleBlock
import hashlib # we hash a bock
import datetime
import os

# Imports to check test it out
from Session1_Fundamentals.block_syncing.task import sync

class Block(SimpleBlock):

    @property
    def header(self):
        """
        To generate a header from a string
        It's just a concatenation of a bunc of things
        This is a function that's used by hash(..) often

        Parameters
        ----------
        nonce : int,
            It's basically a counter
            A counter which moves according to the mine function


        Returns
        -------
        header : str,
            Generates the text of the block header
        """
        return "{}{}{}{}{}".format(
            self.index,
            self.prev_hash,
            self.data,
            self.timestamp,
            self.nonce
        )

    def calculate_hash(self, nonce=0):
        self.nonce = nonce
        header_string = self.header
        # Let's choose something simple for now
        sha_obj = hashlib.sha256()
        sha_obj.update(header_string.encode('utf-8'))
        return sha_obj.hexdigest()

    def update_timestamp(self):
        self.timestamp = "{}".format(datetime.datetime.now())

    def update_hash(self, hash):
        self.hash = hash

    @staticmethod
    def is_valid(block):
        if block.index == 0:
            valid_flag = True
        elif block.hash == block.calculate_hash(block.nonce):
            valid_flag =True
        else:
            print "Validity Condition not satisfied for "
            valid_flag = False
        return valid_flag

def difficulty_condition(hash_to_check):
    NUM_ZEROS=4
    if str(hash_to_check)[0:NUM_ZEROS] == '0'*NUM_ZEROS:
        return True
    else:
        return False

# This should move to class Blockchain in the future
def mine(last_block, NUM_ZEROS=4, data=None):
    """
    Let's take the last block and it's hash
    and mine the next block

    Mining = generating a hash, changing the nonce, till the
             hash which hash NUM_ZEROS number of zeros
    Parameters
    ----------
    last_block : Block or SimpleBlock,
        previous block
    NUM_ZEROS : int,
        How many zeros do we want?

    Returns
    -------

    """
    index = int(last_block.index) + 1  # current block's index = +1 of previous block
    new_block = Block(index=index, data=data, prev_hash=last_block.hash) # Default data for now
    nonce = 0
    while True:
        block_hash = new_block.calculate_hash(nonce)
        # print block_hash, nonce # for now, remove it later
        if difficulty_condition(block_hash):
            new_block.update_hash(block_hash)
            ## WOHOO we cracked a good hash
            # Also, the nonce got updated when we calculated the hash
            break
        else:
            nonce += 1
    return new_block

# Guess why we have this function
# Does sync get the blocks in order??
def get_last_block(all_blocks):
    for block_now in all_blocks:
        if int(block_now.index) == len(all_blocks)-1:
            return block_now


if __name__ == '__main__':
    # # Copy the folder chaindata outside the folder of Blocks
    # folder_chaindata=os.path.abspath(os.path.join(
    #     os.path.dirname(os.path.realpath(__file__)),
    #     "..",
    #     "chaindata"
    # ))
    # Not yet!!
    folder_chaindata = os.path.join("..","chaindata")

    blocks = sync(
        cls=Block,
        chaindata_dir=folder_chaindata
    )
    last_block = get_last_block(blocks)
    new_block = mine(last_block)
    Block.save(new_block.block,folder_chaindata)
    print Block.is_valid(new_block)

