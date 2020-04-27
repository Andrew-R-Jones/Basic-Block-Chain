import struct
import hashlib
from functools import partial
from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone

x = "b2e2b6d064c84eb6bb301fa8a7f6d274"
#b2e2b6d0-64c8-4eb6-bb30-1fa8a7f6d274
x = x[:8] + '-' + x[8:12] + '-' + x[12:16] + '-' + x[16:20] + '-' + x[20:]
print(x)
print("b2e2b6d0-64c8-4eb6-bb30-1fa8a7f6d274")
case_id=UUID(int=0)  # 16 bytes
case_bytes = case_id.int.to_bytes(16, byteorder="little") #or "big
case=UUID(bytes=case_bytes)  # 16 bytes
print(case)
print(case.int)
if case.int == 0:
    print("zero")

