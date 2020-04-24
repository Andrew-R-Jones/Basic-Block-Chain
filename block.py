#import maya
import datetime
import sys
import struct
import hashlib
from collections import namedtuple
from shlex import split
from sys import byteorder
from uuid import UUID, uuid4
import datetime
from datetime import datetime, timedelta, timezone
from functools import partial
import os

def get_current_time():
    return datetime.now().isoformat()
    #return (maya.now()).iso8601()


def get_data_length(data):
    # add 1 for null char
    return len(data.encode('utf-8')) + 1

# block class
class Block: 

    # instantiates block for blockchain
    def __init__(self, previous_hash, case_id, evidence_item_id, state, data=None, data_length=None, time_stamp=get_current_time()):
        self.previous_hash = previous_hash
        self.case_id = case_id
        self.evidence_item_id = evidence_item_id
        self.state = state
        self.data = data
        self.data_length = data_length
        self.time_stamp = time_stamp


    ''' similar to toString, returns info about the object'''
    def __repr__(self):
        return f"{self.previous_hash}\n{self.time_stamp}\n{self.case_id}\n{self.evidence_item_id}\n{self.state}\n{self.data_length}\n{self.data}"

########################################################################################
###############     FOR SUBMISSION      ################################################
#file_path = os.environ["BCHOC_FILE_PATH"]
########################################################################################

########################################################################################
###############     FOR DUBUG AND TESTING       ########################################
#file_path = 'blockchain.txt'
file_path = 'blockchain'
########################################################################################
chain = []
chain_new = []
#create empty file uncomment for testing purposes
#open(file_path, 'w').close()
Block_tuple = namedtuple("Block", ["prev_hash", "timestamp", "case_id", "evidence_id", "state", "d_length", "data"])

STATE = {
    "init": b"INITIAL\0\0\0\0",
    "in": b"CHECKEDIN\0\0",
    "out": b"CHECKEDOUT\0",
    "dis": b"DISPOSED\0\0\0",
    "des": b"DESTROYED\0\0",
    "rel": b"RELEASED\0\0\0",
    "INITIAL": b"INITIAL\0\0\0\0",
    "CHECKEDIN": b"CHECKEDIN\0\0",
    "CHECKEDOUT": b"CHECKEDOUT\0",
    "DISPOSED": b"DISPOSED\0\0\0",
    "DESTROYED": b"DESTROYED\0\0",
    "RELEASED": b"RELEASED\0\0\0",
}

block_head_fmt = "20s d 16s I 11s I"
#block_head_fmt = "20s d 16s I 11s I"
block_head_len = struct.calcsize(block_head_fmt)
block_head_struct = struct.Struct(block_head_fmt)

#making hash into bytes, timestamp to double, casid to bytes, evidence no change
# state bytes, data length no change 
INITIAL = Block_tuple(
    prev_hash=bytes("0","utf-8"),  # 20 bytes
    timestamp=datetime.timestamp(datetime.now()),  # 08 bytes
    case_id=UUID(int=0).int.to_bytes(16, byteorder="little"),  # 16 bytes
    evidence_id=0,  # 04 bytes
    state=STATE["init"],  # 11 bytes
    d_length=14,  # 04 bytes
    data=b"Initial block\0",
)

#pack, write to file, calls add_chain
def pack_block(case,item):
    #check if initial block set hash to zero
    if(len(chain) == 0):
        prev_hash = bytes("0","utf-8")
    else:
        last_block = chain[-1]
        prev_hash = hashlib.sha1(repr(last_block).encode('utf-8')).digest()
    timestamp=datetime.timestamp(datetime.now())
    if case == 0:
        case = "00000000-0000-0000-0000-000000000000"
    case_id = UUID(case).bytes
    evidence=item
    state = STATE["in"]
    d_length=14  # 04 bytes
    data=b"Initial block\0"
    test_pack = block_head_struct.pack(prev_hash,timestamp,case_id,evidence,state,d_length)
    fp = open(file_path, 'ab')
    fp.write(test_pack)
    fp.close()
    add_chain(test_pack)

#prints the chain[]
def print_chain():
    print("printing chain")
    for block in chain_new:
        print(block.prev_hash)
        print(block.timestamp)
        print(block.case_id)
        print(block.evidence_id)
        print(block.state)
        print(block.data)

#adds a block to the chain[]
def add_chain(test_pack):
    blockContents = block_head_struct.unpack(test_pack)
    hash = blockContents[0]
    from binascii import hexlify
    hash= hexlify(hash).decode('ascii')
    timestamp = datetime.fromtimestamp(blockContents[1])
    uuid = UUID(bytes=blockContents[2])
    evidence = blockContents[3]
    state = blockContents[4].decode('utf-8')
    data_len = blockContents[5]
    new_block = Block(hash, timestamp, uuid, evidence, state,data_len,"the data")
    chain.append(new_block)

#not currently in use    
def make_chain():
    chain_new=[]
    with open(file_path, 'rb') as openfileobject:
        for block in iter(partial(openfileobject.read, 68), b''):
            blockContents = block_head_struct.unpack(block)
            hash = blockContents[0]
            from binascii import hexlify
            hash= hexlify(hash).decode('ascii')
            #timestamp = datetime.fromtimestamp(blockContents[1])
            #uuid = UUID(bytes=blockContents[2])
            #evidence = blockContents[3]
            #state = blockContents[4].decode('utf-8')
            #data_len = blockContents[5]
            new_block = Block_tuple(
                prev_hash=hash,  # 20 bytes
                timestamp= datetime.fromtimestamp(blockContents[1]),  # 08 bytes
                case_id=UUID(bytes=blockContents[2]),  # 16 bytes
                evidence_id=blockContents[3],  # 04 bytes
                state=blockContents[4].decode('utf-8'),  # 11 bytes
                d_length=blockContents[5],  # 04 bytes                
                data=b"Initial block\0",
            )
            chain_new.append(new_block)
            #new_block = Block(hash, timestamp, uuid, evidence, state,data_len,"the data")
            #chain.append(new_block)
        openfileobject.close()
        return chain_new
    

#pack_block("00000000-0000-0000-0000-000000000000", 111111111)
#pack_block("65cc391d-6568-4dcc-a3f1-86a2f04140f3", 987654321)
#pack_block("65cc391d-6568-4dcc-a3f1-111111111111", 123445567)
#make_chain()
#print_chain()