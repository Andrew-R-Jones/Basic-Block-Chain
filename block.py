import random
import re
import struct
import subprocess
import unittest
from collections import namedtuple
from copy import deepcopy as copy
from datetime import datetime, timedelta, timezone
from hashlib import sha1
from pathlib import Path
from shlex import split
from subprocess import PIPE, CalledProcessError
from sys import byteorder
from tempfile import TemporaryDirectory
from typing import BinaryIO, List, Callable
from uuid import UUID, uuid4

random.seed()

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

########################################################################################
###############     FOR SUBMISSION      ################################################
file_path = os.environ["BCHOC_FILE_PATH"]
###############     FOR DUBUG AND TESTING       ########################################
#file_path = 'blockchain'
########################################################################################

def get_current_time():
    return datetime.now().isoformat()
    #return (maya.now()).iso8601()

def get_data_length(data):
    # add 1 for null char
    return len(data.encode('utf-8')) + 1

# block class
class Block: 
    # instantiates block for blockchain
    def __init__ (self, previous_hash, case_id, evidence_item_id, state, data, data_length, time_stamp):
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


chain = []
chain_new = []

#Block_tuple = namedtuple("Block", ["prev_hash", "timestamp", "case_id", "evidence_id", "state", "d_length", "data"])
#Block = namedtuple("Block", ["prev_hash", "timestamp", "case_id", "evidence_id", "state", "d_length", "data"])
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
block_head_len = struct.calcsize(block_head_fmt)
block_head_struct = struct.Struct(block_head_fmt)

#making hash into bytes, timestamp to double, casid to bytes, evidence no change
# state bytes, data length no change 


#pack, write to file, calls add_chain
def pack_block(case,item,state,timestamp):
    #======================================================================
    # packing the structure
    #======================================================================
    #we have an initial block that I hard code and then the reg_block
    b=Block(1,2,3,4,5,6,7)
    if(state == "init"):
        data=b"Initial block\0"
        bock_pack = block_head_struct.pack(b"",0,bytes("0", "utf-8"),0,b"INITIAL\0\0\0\0",14,)
        data_pack = struct.pack("14s",data)
        fp = open(file_path, 'ab')
        fp.write(bock_pack)
        fp.write(data_pack)
        fp.close()
    else:
        chain = make_chain()
        last_block = chain[-1]
        b.previous_hash = hashlib.sha1(repr(last_block).encode('utf-8')).digest()
        b.time_stamp=timestamp
        b.case_id=UUID(case).int.to_bytes(16, byteorder="little")  # 16 bytes
        b.evidence_id=item
        b.state = STATE[state]
        b.data = "testing"
        b.data_length = len("testing")
        """
        reg_block = Block(
        prev_hash = hashlib.sha1(repr(last_block).encode('utf-8')).digest(),  # 20 bytes
        timestamp=timestamp,  # 08 bytes
        case_id=UUID(case).int.to_bytes(16, byteorder="little"),  # 16 bytes
        evidence_id=0,  # 04 bytes
        state=STATE[state],  # 11 bytes
        data=b"Initial block\x00",
        d_length=len(data),  # 04 bytes
        )
        """
        #print(b.previous_hash)
        #print(b.time_stamp)
        #print(b.case_id)
        #print(b.evidence_item_id)
        #print(b.state)
        #print(b.data_length)
        block_pack = block_head_struct.pack(
        b.previous_hash,
        b.time_stamp,
        b.case_id,
        b.evidence_item_id,
        b.state,
        b.data_length)

        data_pack = struct.pack("%ds" %(b.data_length),bytes(b.data, "utf-8"))
        #write to file
        fp = open(file_path, 'ab')
        fp.write(block_pack)
        fp.write(data_pack)
        fp.close()
    """
    #check if initial block set hash to zero
    if(len(chain) == 0):
        prev_hash = ""
        prev_hash= prev_hash.encode()
    else:
        last_block = chain[-1]
        prev_hash = hashlib.sha1(repr(last_block).encode('utf-8')).digest()
    #timestamp=datetime.timestamp(datetime.now())
    if case == 0:
        case = "00000000-0000-0000-0000-000000000000"
    case = str(case) #change from UUID to string to do replace
    case = case.replace('-', '') #UUID to bytes does like hyphens
    case_id = UUID(case).bytes 
    evidence=item
    state = STATE[state]
    #d_length=14  # 04 bytes
    data=b"Initial block\x00"
    test_pack = block_head_struct.pack(prev_hash,timestamp,case_id,evidence,state,len(data))  
    fp = open(file_path, 'ab')
    fp.write(test_pack)
    fp.close()
    """

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

#makes the chain   
def make_chain():
    chain_new=[]
    with open(file_path, 'rb') as openfileobject:
        for block in iter(partial(openfileobject.read, 68), b''):
            blockContents = block_head_struct.unpack(block)
            hash = blockContents[0]
            from binascii import hexlify
            hash= hexlify(hash).decode('ascii')
            #hash = hash.decode("utf-8")
            #from binascii import hexlify
            #hash= hexlify(hash).decode('ascii')
            #timestamp = datetime.fromtimestamp(blockContents[1])
            #uuid = UUID(bytes=blockContents[2])
            #evidence = blockContents[3]
            #state = blockContents[4].decode('utf-8')
            #data_len = blockContents[5]
            new_block = Block(1,2,3,4,5,6,7)
            new_block.previous_hash=hash  # 20 bytes
            new_block.time_stamp= datetime.fromtimestamp(blockContents[1])  # 08 bytes
            new_block.case_id=UUID(bytes=blockContents[2])  # 16 bytes
            new_block.evidence_item_id=blockContents[3]  # 04 bytes
            new_block.state=blockContents[4].decode('utf-8')  # 11 bytes
            new_block.data_length=blockContents[5]  # 04 bytes                
            new_block.data = ""
            d_raw = openfileobject.read(new_block.data_length)
            x = struct.unpack("%ds" % (new_block.data_length), d_raw)
            new_block.data = x[0]
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