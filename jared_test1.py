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
length = 20
data = "just gonna leave this hear"
data = bytes(data,'utf-8')
block_test = pack('sdqqisis',hash,timestamp,case_id_front,case_id_back,evidence_id,state,length,data)
a,b,c,d,e,f,g,h = unpack('sdqqisis', block_test)
print("a: ", a, " b: ", b, " c:", c, " d:", d, " e:" ,e, "f: " ,f, "g:" , g, "h: ", h)
string = "Python"

# string with encoding 'utf-8'
arr = bytes(string, 'utf-8')
print(arr)
arr1 = arr.decode("utf-8")
print(arr1)
tester = pack('10s',arr)
ret = unpack('10s',tester)
#print(ret1)
print("doing some bit shifting")
str5 = "123456"
str1 = str5[:3]
str2 = str5[3:]
str2 = int(str2)
str1 = int(str1)
test = pack('qq', str1,str2)
j,k = unpack('qq',test)
print("j:", j, " k:", k)
comb = str(j) + str(k)

print("str1: ", str1, "binar: ", bin(str1))
print("str2: ", str2, "binar: ", bin(str2))
print("combined ", comb)
