# TODO: type solution here
from Session1_Fundamentals.block_basics.simpleblock import SimpleBlock


# lets read some blocks and do something on it
import json, os


def sync_local(cls=SimpleBlock, chaindata_dir='chaindata'):
    node_blocks = []
    if not os.path.isabs(chaindata_dir):
        folder_here =os.path.dirname(os.path.realpath(__file__))
        chaindata_dir = os.path.join(folder_here, chaindata_dir)

    # Lets scan the folder
    for filename in os.listdir(chaindata_dir):
        abs_filename = os.path.join(
            chaindata_dir,
            filename
        )
        # looking for only the json files
        if os.path.splitext(filename)[-1] == '.json':
            with open(abs_filename, "r") as block_file:
                block_dict = json.load(block_file)
                cur_block = cls.load_from_dict(block_dict)
                # Just print a debug message for now
                if cls.is_valid(cur_block):
                    node_blocks.append(cur_block)
                # Ideally we shouldn't update node_blocks if hash doesn't match

    return node_blocks

def sync(cls=SimpleBlock, chaindata_dir='chaindata'):
    return sync_local(
        cls=cls,
        chaindata_dir=chaindata_dir
    )

if __name__ == '__main__':
    peer_nodes = sync(cls=SimpleBlock)
    print peer_nodes
