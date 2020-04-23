# *-* coding: utf-8 *-*
import hashlib
import sys
import struct
from collections import namedtuple
from uuid import UUID, uuid4
import datetime

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
    prev_hash=0,  # 20 bytes
    timestamp=0,  # 08 bytes
    case_id=UUID(int=0),  # 16 bytes
    evidence_id=0,  # 04 bytes
    state=STATE["init"],  # 11 bytes
    d_length=14,  # 04 bytes
    data=b"Initial block\0",
)

block_head_fmt = "20s d 16s I 11s I"
block_head_len = struct.calcsize(block_head_fmt)
block_head_struct = struct.Struct(block_head_fmt)

#fp = open('./test003','rb')
#======================================================================
# Unpacking the block structure
#======================================================================
#block = fp.read(68)
#blockContents = block_head_struct.unpack(block)
#timestamp = datetime.fromtimestamp(blockContents[1])

# print(timestamp)
# print(blockContents)

# fp.close()


#======================================================================
# packing the structure
#======================================================================
prev_hash = hashlib.sha1().digest()
print(prev_hash)
timestamp=3.21  # 08 bytes
case_id=UUID(int=0)  # 16 bytes
case_bytes = case_id.int.to_bytes(16, byteorder="little") #or "big
evidence_id=0  # 04 bytes
state=STATE["init"]  # 11 bytes
d_length=14  # 04 bytes
data=b"Initial block\0"
test_struct = block_head_struct.pack(prev_hash,timestamp,case_bytes, evidence_id,state,len(data))
#test_struct =struct.pack("20s d 16s i 11s i",prev_hash,timestamp,case_bytes, evidence_id,state,len(data))

#===================================
# saving to txt file
#===================================
fp = "test.txt"
print(test_struct)
with open(fp, 'w') as filehandle:
        filehandle.write('%s\n' % test_struct)
        filehandle.close()

#=====================================
#reading from txt file
#====================================
with open(fp, 'r') as filehandle:
    b1 = filehandle.read(68)
    filehandle.close()
print(b1)

#=======================================
# upacking contents
#======================================

blockContents = block_head_struct.unpack(bytes(b1, 'utf-8'))
hash = blockContents[0]
from binascii import hexlify
hash= hexlify(hash).decode('ascii')
second = blockContents[1]
print(second)
#timestamp = datetime.datetime.fromtimestamp(blockContents[1])
#print(timestamp)
