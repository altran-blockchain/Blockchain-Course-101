# TODO: type solution here
from Session1_Fundamentals.block_syncing.task import sync
from flask import Flask
import pprint

node = Flask(__name__)


@node.route('/blockchain', methods=['GET'])
def blockchain():
    """
    Deplots our blockchain
    Lists of json of hashes of block info =
    [index, timestamp, data, hash, prev_hash]
    """

    node_blocks = sync()

    # Convert our blocks into dictionaries
    blocks_to_show = dict()

    for block in node_blocks:
        blocks_to_show[block.index] = block.block

    return pprint.pformat(blocks_to_show)


if __name__ == '__main__':
    node.run()
