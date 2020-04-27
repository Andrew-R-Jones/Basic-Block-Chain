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
debug = False
###############     FOR DUBUG AND TESTING       ########################################
#file_path = 'blockchain'
#debug = True
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

#pack and write to file
def pack_block(case,item,state,timestamp, data):
    #======================================================================
    # packing the structure
    #======================================================================
    #we have an initial block that I hard code and then the reg_block
    b=Block(1,2,3,4,5,6,7)
    if(state == "INITIAL"):
        data=b"Initial block\0"
        case_id=UUID(int=0)  # 16 bytes
        case_bytes = case_id.int.to_bytes(16, byteorder="little") #or "big"
        bock_pack = block_head_struct.pack(b"",timestamp,case_bytes,0,b"INITIAL\0\0\0\0",14,)
        data_pack = struct.pack("14s",data)
        fp = open(file_path, 'ab')
        fp.write(bock_pack)
        fp.write(data_pack)
        fp.close()
    else:
        chain = make_chain()
        last_block = chain[-1]
        if debug:
            print("-----last block-------")
            print(last_block.previous_hash)
            print("timestamp:",last_block.time_stamp)
            print("caseID:",last_block.case_id)
            print("evidenceID:",last_block.evidence_item_id)
            print("state:",last_block.state)
            print("data len:",last_block.data_length)
            print("data:",last_block.data)
            print("------------------------------")
        #forcing it to work
        b.previous_hash = hashlib.sha1(repr(last_block).encode('utf-8')).digest()
        if debug:
            print("state:"+last_block.state.strip(' \t\r\n\0')+":" )
            print(last_block.state.strip(' \t\r\n\0') == "INITIAL")
        #if(last_block.state == "INITIAL"):
        #    b.previous_hash = b''
        b.time_stamp=timestamp
        case_uuid = UUID(str(case))
        case_bytes = case_uuid.int.to_bytes(16, byteorder="little") #or "big"
        b.case_id=case_bytes
        b.evidence_item_id=item
        b.state = STATE[state]
        b.data = data
        b.data_length = len(b.data)
        if debug:
            print("----------PACKING----------")
            print("Hash:", b.previous_hash)
            print("timestamp:",b.time_stamp)
            print("caseID:",b.case_id)
            print("evidenceID:",b.evidence_item_id)
            print("state:",b.state)
            print("data len:",b.data_length)
            print("data:",b.data)
            print("------------------------------")
        #pack block
        block_pack = block_head_struct.pack(
        b.previous_hash,
        b.time_stamp,
        b.case_id,
        b.evidence_item_id,
        b.state,
        b.data_length)
        #pack data
        data_pack = struct.pack("%ds" %(b.data_length),bytes(b.data, "utf-8"))
        #write to file
        fp = open(file_path, 'ab')
        fp.write(block_pack)
        fp.write(data_pack)
        fp.close()
   
#makes the chain   
def make_chain():
    chain=[]
    with open(file_path, 'rb') as openfileobject:
        #if you cannot get68 bytes
        try:
            for block in iter(partial(openfileobject.read, 68), b''):
                blockContents = block_head_struct.unpack(block)
                blockContents = block_head_struct.unpack(block)
                hash = blockContents[0]
                from binascii import hexlify
                hash= hexlify(hash).decode('ascii')
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
                if debug:
                    print("----------makechain()----------")
                    print("Hash:", new_block.previous_hash)
                    print("timestamp:",new_block.time_stamp)
                    print("caseID:",new_block.case_id)
                    print("evidenceID:",new_block.evidence_item_id)
                    print("state:",new_block.state)
                    print("data len:",new_block.data_length)
                    print("data:",new_block.data)
                    print("------------------------------")
                chain.append(new_block)
            openfileobject.close()
            return chain
        except:
            print("corrupted block")
            exit(1)
        
            