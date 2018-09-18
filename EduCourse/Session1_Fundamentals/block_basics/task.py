# This file creates the block structure
# and writes the first file

import datetime
import os, json

class SimpleBlock(object):
    def __init__(self,
                 index=0,
                 timestamp=None,
                 prev_hash=None,
                 data=None,
                 hash=None,
                 nonce=0):
        self.index = index

        # to create a string from a bunch of different
        # types of variables.
        # The same as a str(timestamp), but cleaner
        if timestamp is None:
            # Ideally a block is created during mining
            # and we will pass a value
            # we don't need to use this except
            # for the "genesis" block
            self.timestamp = "{}".format(
                datetime.datetime.now()
            )
        # loading the hash
        else:
            self.timestamp=timestamp
        self.prev_hash = prev_hash
        if not data:
            self.data = data
        else:
            self.data = self.default_data(index)

        if not hash:
            self.hash = self.stupid_hash
        else:
            self.hash = hash

        self.nonce = nonce # We'll get back to this later

    @property
    def block(self):
        """
        This is a property.
        That means I don't have to call this as a function
        it acts like a getter variable.
        :return:
        """
        return {
            "index" : self.index,
            "timestamp": self.timestamp,
            "prev_hash": self.prev_hash,
            "data": self.data,
            "hash": self.hash,
            "nonce": self.nonce,
        }

    @property
    def stupid_hash(self):
        """
        Generate the hash over the current block

        Parameters
        ----------
        nonce

        Returns
        -------

        """
        return "hash placeholder"

    @staticmethod
    def default_data(index):
        return "I am in block {}".format(index)

    @staticmethod
    def save(block_to_write, chaindata_dir):
        filename = "{}.json".format(block_to_write["index"])
        if not os.path.isabs(chaindata_dir):
            my_dir = os.path.dirname(__file__)
            chaindata_dir = os.path.join(
                my_dir,
                chaindata_dir
            )
        filename_abs = os.path.join(
            chaindata_dir,
            filename
        )
        with open(filename_abs, "w") as f:
            print "Writing block with index : {} to {}".format(
                block_to_write["index"],
                filename_abs
            )
            f.write(
                json.dumps(block_to_write, indent=4, sort_keys=True)
            )

        pass # do nothing for now

    @classmethod
    def load_from_dict(cls, dict_to_load):
        if "index" not in dict_to_load:
            dict_to_load["index"] = None
        my_obj = cls(
            index = dict_to_load['index'],
            timestamp=dict_to_load['timestamp'],
            prev_hash=dict_to_load['prev_hash'],
            hash=dict_to_load['hash'],
            data=dict_to_load['data'],
            nonce=dict_to_load['nonce']
        )
        return my_obj

    @staticmethod
    def is_valid(block):
        return True  # All blocks are valid. HAHAHAHAH

    # to display some info when I say print my_block
    def __str__(self):
        return "Block info <prev_hash:{}> , <my_hash:{}>".format(self.prev_hash,
                                                                 self.hash)
    def __repr__(self):
        return "Block info <prev_hash:{}> , <my_hash:{}>".format(self.prev_hash,
                                                                 self.hash)
    # To check equality
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

def prepare_folder(folder_chaindata="chaindata"):
    if os.path.isabs(folder_chaindata):
        folder_chaindata_abs = folder_chaindata
    else:
        folder_here =os.path.dirname(os.path.realpath(__file__))
        folder_chaindata_abs = os.path.join(folder_here, "..", folder_chaindata)

    print "Going to make the chaindata here", folder_chaindata_abs
    if not os.path.exists(folder_chaindata_abs):
        os.mkdir(folder_chaindata_abs)

if __name__ == '__main__':
    # Some tests
    prepare_folder(os.path.join("..",'chaindata'))
    test_block = SimpleBlock(
        index=0,
        data="MY first block, woohoo",
        prev_hash = None # Only the first block doesn't need prev_hash
    )

    print test_block.block
    test_block.save(test_block.block, os.path.join("..","chaindata"))
