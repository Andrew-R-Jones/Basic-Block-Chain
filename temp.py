import struct
import hashlib
from functools import partial

#hash, time, caseid, evidence, state, length, data
block_head_fmt = "20sxxxx d 16s I 11sx I" #20+8+16+4+11+4=63 add padd
#block_head_fmt = "20s d 16s I 11s I"
block_head_len = struct.calcsize(block_head_fmt)
block_head_struct = struct.Struct(block_head_fmt)

def test_pack():
    x = bytes("0", "utf-8")
    y = "0"
    y = y.encode()
    t1 = struct.pack("20s", y)
    print(t1)
    t2 = struct.unpack("20s",t1)
    #from binascii import hexlify
    #hash= hexlify(t2[0]).decode('ascii')
    #hash = t2[0].decode("utf-8")
    print(hash)
def test_003():
        #82
        d_length = 14
        data = "what"
        block_head_fmt = "20s d 16s I 11s I s" 
        
        with open('test003', 'rb') as openfileobject:
            x = openfileobject.read()
            print(x)
            
            #y = struct.unpack("20s d 16s I 11s I",x)
            #blockContents = block_head_struct.unpack(x)
            #for block in iter(partial(openfileobject.read, 68), b''):
             #   blockContents = block_head_struct.unpack(block)
                #hash = blockContents[0]
                #hash = hash.decode("utf-8")
                #print(blockContents)
#test_003()
def t2():
    s = "test1"
    s = bytes(s, 'utf-8')    # Or other appropriate encoding
    struct.pack("I%ds" % (len(s),), len(s), s)
    a = 4
    x = struct.pack("I%ds" % (len(s)), a, s)
    y = struct.unpack("I 5s", x)
    b = struct.pack("s", s)
    c = struct.unpack("s", b)
    print(c)
    #struct.error: unpack requires a buffer of 68 bytes
t2()






#pack, write to file, calls add_chain
def pack_block(case,item,state,timestamp):
    #check if initial block set hash to zero
    if(len(chain) == 0):
        prev_hash = bytes("0","utf-8")
    else:
        last_block = chain[-1]
        prev_hash = hashlib.sha1(repr(last_block).encode('utf-8')).digest()
    #timestamp=datetime.timestamp(datetime.now())
    if case == 0:
        case = "00000000-0000-0000-0000-000000000000"
    case = str(case) #change from UUID to string to do replace
    case = case.replace('-', '') #UUID to bytes does like hyphens
    case_id = UUID(case).bytes 
    evidence=item
    state = STATE[state]
    d_length=14  # 04 bytes
    data=b"Initial block\x00"
    test_pack = block_head_struct.pack(prev_hash,timestamp,case_id,evidence,state,d_length)
    fp = open(file_path, 'ab')
    fp.write(test_pack)
    fp.close()
    print(test_pack)
#pack_block(0,0, "init", 0)
#test_pack()
