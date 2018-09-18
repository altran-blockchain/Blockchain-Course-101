# TODO: type solution here
from Session1_Fundamentals.block_mining.task import Block
import os
import json

class Blockchain(object):

    def __init__(self, blocks):
        assert blocks is None or isinstance(blocks, list)
        # We want to only load blockchain with valid blocks
        self.blocks = [b for b in blocks if Block.is_valid(b)] or []
        self.sort()

    def sort(self):
        self.blocks.sort(key=lambda b: int(b.index))

    # Just like block_2.sync
    @classmethod
    def load(cls, data_dir):
        blocks = []
        if os.path.exists(data_dir):
            for filename in os.listdir(data_dir):
                if os.path.splitext(filename)[-1] == ".json":
                    rel_path = os.path.join(data_dir, filename)
                    with open(rel_path, 'r') as block_file:
                        block_info = json.load(block_file)
                        block = Block.load_from_dict(block_info)

                        # Check for block validity.
                        # discarding all garbage
                        if Block.is_valid(block):
                            blocks.append(block)
        return cls(blocks)

    def is_valid(self):
        '''
        Got to check if chain is valid. By :-
        1) Each block is indexed in order
        2) prev_hash of each block = hash of previous block
        3) block's hash is valid --> This has already been done in the loading
            We assume our blockchain contains "clean" blocks
        '''
        for index in range(1,len(self)):
            prev_block = self.blocks[index - 1]
            cur_block = self.blocks[index]
            # print (index)
            # print (prev_block, cur_block)
            # Check all three conditions
            # print (prev_block.index, cur_block.index)

            if prev_block.index + 1 != cur_block.index:
                print ("Index dont match")
                return False
            if prev_block.hash != cur_block.prev_hash:
                print "Problematic Hash order in chain :", (prev_block.hash, cur_block.hash)
                return False
        return True

    def save(self, chaindata_dir):
        for b in self.blocks:
            Block.save(b, chaindata_dir=chaindata_dir)
        return True

    # Does this make sense bro?
    def find_block_by_index(self, index):
        if len(self.blocks) <= index:
            return self.blocks[index]
        else:
            return False

    def find_block_by_hash(self, hash):
        for b in self.blocks:
            if b.hash == hash:
                return b
        return False

    def add_block(self, new_block):
        if Block.is_valid(new_block):
            new_block.index = len(self)
            self.blocks.append(new_block)
        return True

    def list_of_blocks(self):
        return [b.block for b in self.blocks]

    # Some operators
    def __len__(self):
        return len(self.blocks)

    def __eq__(self, other):
        return self.blocks == other.blocks

    def __gt__(self, other):
        return len(self.blocks) > len(other.blocks)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)


if __name__ == "__main__":
    folder_chaindata=os.path.abspath(os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..",
        "chaindata"
    ))
    my_blockchain = Blockchain.load(folder_chaindata)
    other_blockchain = Blockchain.load(folder_chaindata)
    print my_blockchain == other_blockchain

    # Try to play around here.
    # Delete the last block and add it's contents manually
    # Then check if the block is valid

    # Go back to the broadcast task and
    # run it again and see what we have :)
    print my_blockchain.is_valid()
    pass
