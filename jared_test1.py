import sys
import struct
import hashlib
from collections import namedtuple
from shlex import split
from sys import byteorder
from uuid import UUID, uuid4
import datetime
from datetime import datetime, timedelta, timezone

##trying to pack and upack the intial block and compare against test003
# *-* coding: utf-8 *-*

Block = namedtuple("Block", ["prev_hash", "timestamp", "case_id", "evidence_id", "state", "d_length", "data"])

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
INITIAL = Block(
    prev_hash=bytes("0","utf-8"),  # 20 bytes
    timestamp=datetime.timestamp(datetime.now()),  # 08 bytes
    case_id=UUID(int=0).int.to_bytes(16, byteorder="little"),  # 16 bytes
    evidence_id=0,  # 04 bytes
    state=STATE["init"],  # 11 bytes
    d_length=14,  # 04 bytes
    data=b"Initial block\0",
)

block_head_fmt = "20sxxxx d 16s I 11sx I"
#block_head_fmt = "20s d 16s I 11s I"
block_head_len = struct.calcsize(block_head_fmt)
block_head_struct = struct.Struct(block_head_fmt)

fp = open('./test003','rb')

#======================================================================
# Unpacking the block structure
#======================================================================
block = fp.read(68)
blockContents = block_head_struct.unpack(block)
timestamp = datetime.fromtimestamp(blockContents[1])
print("printing 003 block")
print(block)
print("printing 003 contents")
print(blockContents)
fp.close()


#======================================================================
# packing the structure
#======================================================================
"""
block_bytes = block_head_struct.pack(
    prev_hash,
    block.timestamp,
    block.case_id.int.to_bytes(16, byteorder="little"), #or "big"
    block.evidence_id,
    state,
    len(data),
)
"""
#packing with intial data
test_pack = block_head_struct.pack(INITIAL[0],INITIAL[1],INITIAL[2],INITIAL[3],INITIAL[4],INITIAL[5])
fp = open("./test004", 'wb')
fp.write(test_pack)
fp.close()

#unpack and compare
fp = open('./test004','rb')

#======================================================================
# Unpacking the block structure
#======================================================================
block = fp.read(68)
blockContents = block_head_struct.unpack(block)
timestamp = datetime.fromtimestamp(blockContents[1])
print("printing 004 block")
print(block)
print("printing 004 block contents")
print(blockContents)