import collections
import struct
import sys
import os
import os.path
def packDataPack(output_file):
  rootdir = b"F:\Pak\Unpack"
  k={}
  for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
      k[int(filename[:filename.find(b".")])]=os.path.join(parent,filename)
  k=sorted(k.items(),key=lambda d:d[0])
  num = 0
  data = b''
  edata = b''
  kdata = b''
  eu = 0
  for (id,fn) in  k:
    num += 1
    uc = open(fn,'rb')
    ka = uc.read()
    data += ka
    edata += struct.pack("<HI", id, eu)
    eu += len(ka)
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