import collections
import struct
import sys
import os
import json
def UnpackDataPack(input_file):
    uc = open(input_file,'rb')
    data = uc.read()
    original_data = data
    version, num_entries, encoding = struct.unpack("<IIB", data[:9])
    if version != 4:
        raise Exception("Wrong file version in ", input_file)
    data = data[9:]
    infos={}
    for _ in range(num_entries):
        id, offset = struct.unpack("<HI", data[:6])
        data = data[6:]
        next_id, next_offset = struct.unpack("<HI", data[:6])
        infos[str(id)]=original_data[offset:next_offset].decode('utf-8')
    of = open('Unlang.json','w',encoding='utf-8')
    json.dump(infos,of,indent=4,ensure_ascii=False)
    of.close()
def main():
    if len(sys.argv) > 1:
        os.chdir(sys.path[0])
        UnpackDataPack(sys.argv[1])
if __name__ == '__main__':
    main()