from struct import *
import sys
"""
20 byte string previsou hash = 20s = 20 byte string 
8 byte float timestamp = d 8 byte float
16 byte int case_id = UUID
4 byte int evidence_id
11 byte string state
4 byte int length
0 - 4.2 gig 2^32 string data undefined length
128bit UUID, structs can only have 64 bits q long long unsigned. send 2 unisgned 64 bit ints and then
unpack them using bit shifting. we cant use strings because its 32 character hence 32 bytes needs to
be 16 bytes.sdqqisis
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
data = bytes(data,'utf-8')
block_test = pack('20sdqqi11si%ds'% (length),hash,timestamp,case_id_front,case_id_back,evidence_id,state,length,data)
a,b,c,d,e,f,g,h = unpack('20sdqqi11si%ds'% (length), block_test)
print(block_test)
print("a: ", a, " b: ", b, " c:", c, " d:", d, " e:" ,e, "f: " ,f, "g:" , g, "h: ", h)

#unpack
unpack_hash = a.decode("utf-8")
unpack_timestamp = b
unpack_case_id = str(c) + str(d)
unpack_evidence = e
unpack_state = f.decode("utf-8")
unpack_length = g
unpack_data = h.decode("utf-8")
print("hash decode: ", unpack_hash)
print("timestamp decode", unpack_timestamp)
print("case_id decode: ", unpack_case_id)
print("evidence: ", unpack_evidence)
print("state: ", unpack_state)
print("length: ", unpack_length)
print("data: ", unpack_data)