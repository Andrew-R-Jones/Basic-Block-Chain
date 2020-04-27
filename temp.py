import struct
import hashlib
from functools import partial
from uuid import UUID, uuid4

#hash, time, caseid, evidence, state, length, data
block_head_fmt = "20s d 16s I 11s I"
block_head_len = struct.calcsize(block_head_fmt)
block_head_struct = struct.Struct(block_head_fmt)
struct.pack("0s",b"")
#case_id=UUID(int=case)  # 16 bytes
#case_bytes = case_id.int.to_bytes(16, byteorder="little") #or "big"
#print(case_id)
#print(case_bytes)
#upack = UUID(bytes=case_bytes)
#print(upack)
#bchoc add -c 65cc391d-6568-4dcc-a3f1-86a2f04140f3 -i 987654321 -i 123456789
case = "65cc391d-6568-4dcc-a3f1-86a2f04140f3"
case=case[len(case)::-1] # method
case_id=UUID(case)
case_bytes = case_id.bytes # 16 bytes little indian
upack = UUID(bytes=case_bytes)
print(upack)
#0f13fdc9-7333-4dd0-af33-3efa985806c9 caseID
#c9065898-fa3e-33af-d04d-3373c9fd130f this is what prints out. 
case=case[len(case)::-1] # method 
#print(rev)
#1200ee0d-027b-48f4-99ad-c87ff83f94d1
t1="1200ee0d-027b-48f4-99ad-c87ff83f94d1"
t2 = UUID(t1)
t3 = t2.int.to_bytes(16, byteorder="little") #or "big"
print(t3)
t4 = UUID(bytes=t3)
print(t4)
#t1.int.to_bytes(16, byteorder="little") #or "big"
print("while")
l = [3,4]
while(len(l) != 0):
    print(l[0])
    print(l[1])
    l.pop(0)
    l.pop(0)
print("and we are out")