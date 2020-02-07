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
data = "just gonna leave this hear"
length = len(data)
data = bytes(data,'utf-8')
#block_test = pack('20sdqqi11si26s',hash,timestamp,case_id_front,case_id_back,evidence_id,state,length,data)
#a,b,c,d,e,f,g,h = unpack('20sdqqi11si26s', block_test)
block_test = pack('20sdqqi11si26s',hash,timestamp,case_id_front,case_id_back,evidence_id,state,length,data)
a,b,c,d,e,f,g,h = unpack('20sdqqi11si26s', block_test)
print("a: ", a, " b: ", b, " c:", c, " d:", d, " e:" ,e, "f: " ,f, "g:" , g, "h: ", h)

#unpack
unpack_hash = a.decode("utf-8")
unpack_timestamp = b
unpack_case_id = str(case_id_front) + str(case_id_back)
print("hash decode: ", unpack_hash)
print("timestamp decode", unpack_timestamp)
print("case_id decode: ", unpack_case_id)

#I need help with the string conversion I am strugling understanding it
#On stack overflow I found a solution but I dont understand % workings
#to get the struct completed I need to add padding(easy), double check the bytes are correct
# and finish variable length string"data" below is a working example of variable length string packed. I dont
# know how to unpack I am confused by the %.

str5 = "going to test this"
str5 = bytes(str5,'utf-8')
str5_len = len(str5)
print("str5_len", str5_len)
val = pack('i%ds' % (len(str5),), len(str5), str5)
#unpack_val = unpack('i%ds',val)  #this doesn't work