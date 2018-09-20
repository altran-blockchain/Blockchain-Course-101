from block import Block
import json
import os
import requests
import time
import glob
import datetime

class BlockChain(object):
    def __init__(self, blocks=None): # , data_dir=None, json_string=None):
        assert blocks is None or isinstance(blocks, list)
        self.blocks = blocks or []

    @staticmethod
    def new_block(*args, **kwargs):
        """Contructs a block of a class compatible with this BlockChain class
        with the specified arguments"""
        return Block(*args, **kwargs)
        
    @classmethod
    def load(cls, data_dir):
        bchain = cls()
        if os.path.exists(data_dir):
            for filepath in glob.glob(os.path.join(data_dir, "*.json")):
                with open(filepath, 'r') as block_file:
                    block_info = json.load(block_file)
                    bchain.append(bchain.new_block(**block_info))
        bchain.blocks.sort(key=lambda b: int(b.index))
        return bchain        
    
    # @staticmethod
    # def from_json(json_string):
    #     return BlockChain([Block(**s) for s in json.loads(json_string)])
    
    @classmethod
    def from_url(cls, url):
        """This function expects a url from which a json encoding a 
        blockchain will be returned."""
        chaindata = requests.get(url).json()
        return cls([cls.new_block(**blockdata) for blockdata in chaindata])

    def as_json(self):
        return json.dumps([block.__dict__ for block in self.blocks])
    
    def is_valid(self, difficulty):
        """
        Is a valid blockchain if

        1) Each block is indexed one after the other
        2) Each block's prev hash is the hash of the prev block
        3) The block's hash is valid for the number of zeros

        Not taken into account but could be relevant:

        4) Conditions on the timestamps
        5) Difficulty depending on the timestamps of previous blocks
        """
        if not self.blocks:
            return True
        if self.blocks[0].index != 0:
            return False
        for (prev_block, block) in zip(self.blocks[:-1], self.blocks[1:]):
            if not block.is_valid():
                return False
            if not block.satisfies_pow(difficulty):
                return False
            if not prev_block.is_valid_predecessor(block):
                return False
        return self.blocks[0].satisfies_pow(difficulty) and self.blocks[0].is_valid()
  
    def save(self, data_dir):
        """
        Save each block in this chain (the filename only depends on the index).
        """
        for block in self.blocks:
            block.save(data_dir)
  
    def head(self):
        return None if len(self) == 0 else self.blocks[-1]
      
    # def is_valid_extension(self, block):
    #     return True if not self.blocks else \
    #         self.head().is_valid_predecessor(block)

    def __len__(self):
        return len(self.blocks)

    def __eq__(self, other):
        return self.blocks == other.blocks

    def __ne__(self, other):
        return not self == other

    def next_index(self):
        return 0 if len(self) == 0 else self.head().index + 1
        
    def mine(self, data, difficulty, intents=1000):
        """Try to mine a next block for the given difficulty by computing 
        the specified number of hashes.
        With the strategy used here the nonce is never very high, but that 
        doesn't matter. 
        The change in the timestamp in different calls will cause the hashes 
        to be different every time, even for the same nonces.
        If no valid block is found in the given number of intents, None is 
        returned.
        """
        if data is None:
            return None
        timestamp = datetime.datetime.utcnow().isoformat()
        prev_hash = "" if len(self) == 0 else self.head().get_hash()
        block = self.new_block(index=self.next_index(), timestamp=timestamp,
                               data=data, prev_hash=prev_hash, nonce=0)
    
        for nonce in range(intents):
            block.nonce = nonce
            if block.satisfies_pow(difficulty):
                return block
            time.sleep(0.01)
        return None

    def append(self, block):
        """Extend the blockchain with a new block. It is not checked that 
        the blockchain is still valid"""
        self.blocks.append(block)

    def pop(self):
        return self.blocks.pop()
        
    def __getitem__(self, index): # index may be a slice
        return self.blocks[index]

    def __iter__(self):
        return self.blocks.__iter__()
        
    def forkpoint(self, other):
        """return n if the blockchains are different from node n onward 
        (first n, numbered 0,...,n-1, are equal) or -1 if everywhere 
        different"""
        def _forkpoint(b1, b2, n):
            return n if b1[0] != b2[0] else _forkpoint(b1[1:], b2[1:], n+1)
        if self[0] != other[0]:
            return -1
        else:
            return _forkpoint(self, other, 1)

