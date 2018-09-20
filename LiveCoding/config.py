from ecdsa import NIST192p as CURVE
DATA_DIR = 'blockchaindata'
NODE_ADDRESSES = ["localhost:5000", "localhost:5001", "localhost:5002", "localhost:5003"]
DIFFICULTY = 3 # leading zeros
CONFIRMATIONS = 6 # number of confirmations before considering a transaction final
BLOCK_REWARD = 1
MAX_TRANSACTIONS_PER_BLOCK = 5
NEW_ADDRESS_BALANCE = 1 # the amount that a newly created address gets assigned

# Not used anymore
# LEASE_TIME = 60 # how long the tracker keeps you registered in seconds
# CHAINDATA_DIR = 'chaindata'
# MEMPOOL_ADDRESS = "localhost:5100"
# TRACKER_ADDRESS = "localhost:5000"
# TRACKER_ADDRESSES = ["localhost:5000", "localhost:5001", "localhost:5002", "localhost:5003"]
# from blockchain import BlockChain as BLOCKCHAIN_CLASS
# from transaction import TransactionBlockChain as BLOCKCHAIN_CLASS
