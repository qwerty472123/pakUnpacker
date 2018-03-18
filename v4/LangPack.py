import collections
import struct
import sys
import os
import json

def packDataPack(output_file):
    num = 0
    data = b''
    edata = b''
    kdata = b''
    eu = 0
    hf = open('Unlang.json','r',encoding='utf-8')
    content=json.load(hf)
    hf.close()
    for info in content:
        num += 1
        k = content[info].encode('utf-8')
        data += k
        edata += struct.pack("<HI", int(info), eu)
        eu += len(k)
    pc = 15+len(edata)
    edata += struct.pack("<HI",0, len(data))
    
    for _ in range(num+1):
        id,off = struct.unpack("<HI",edata[:6])
        edata=edata[6:]
        kdata += struct.pack("<HI", id,off+pc)
    of = open(output_file,'wb')
    of.write(struct.pack("<IIB",4,num,1)+kdata+data)
    of.close()
def main():
    if len(sys.argv) > 1:
        os.chdir(sys.path[0])
        packDataPack(sys.argv[1])
if __name__ == '__main__':
    main()