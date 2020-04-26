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

