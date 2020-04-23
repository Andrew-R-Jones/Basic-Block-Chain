import sys
import struct
import hashlib
from collections import namedtuple
from shlex import split
from sys import byteorder
from uuid import UUID, uuid4
import datetime
"""
hash = "12345678901234567890" #20byte length hash
hash = bytes(hash, 'utf-8')
timestamp = 3.234234 #8 byte float timestamp
case_id = "11111222223333344444555556666677" #32 character UUID "128 bit int"
case_id_front = case_id[:16]
case_id_back = case_id[16:]
case_id_front = int(case_id_front)
case_id_back = int(case_id_back)
evidence_id = 123456
state = "CHECKEDIN"
state = bytes(state, 'utf-8')
data = "just gonna leave this here"
length = len(data)
data = bytes(data, 'utf-8')
block_test = pack('20sdqqi11si%ds'% (length),hash,timestamp,case_id_front,case_id_back,evidence_id,state,length,data)
a,b,c,d,e,f,g,h = unpack('20sdqqi11si%ds'% (length), block_test)
#print(block_test)
#print("a: ", a, " b: ", b, " c:", c, " d:", d, " e:" ,e, "f: " ,f, "g:" , g, "h: ", h)
#print(type(a))
#unpack
unpack_hash = a.decode("utf-8")
unpack_timestamp = b
unpack_case_id = str(c) + str(d)
unpack_evidence = e
unpack_state = f.decode("utf-8")
unpack_length = g
unpack_data = h.decode("utf-8")
#print("hash decode: ", unpack_hash)
#print("timestamp decode", unpack_timestamp)
#print("case_id decode: ", unpack_case_id)
#print("evidence: ", unpack_evidence)
#print("state: ", unpack_state)
#print("length: ", unpack_length)
#print("data: ", unpack_data)
#print("new!!!!!!!!!!!!!!!!")
# *-* coding: utf-8 *-*

"""

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
# fp = open('./test003','rb')
hash = hashlib.sha1().digest()
timestamp = 3.234234 #8 byte float timestamp
case_id=int((UUID(int=0))) # 16 bytes
evidence_id=0  # 04 bytes
state=STATE["init"]  # 11 bytes
d_length=14,  # 04 bytes

#block_head_struct.pack(hash,timestamp,case_id,evidence_id,state,d_length)



#======================================================================
# Unpacking the block structure
#======================================================================
#block = fp.read(68)
#blockContents = block_head_struct.unpack(block)
#timestamp = datetime.fromtimestamp(blockContents[1])

# print(timestamp)
# print(blockContents)

# fp.close()
