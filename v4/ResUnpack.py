import collections
import struct
import sys
import os
def UnpackDataPack(input_file):
  uc = open(input_file,'rb')
  data = uc.read()
  original_data = data
  version, num_entries, encoding = struct.unpack("<IIB", data[:9])
  if version != 4:
    raise Exception("Wrong file version in ", input_file)
  data = data[9:]
  for _ in range(num_entries):
    id, offset = struct.unpack("<HI", data[:6])
    data = data[6:]
    next_id, next_offset = struct.unpack("<HI", data[:6])
    filetype = 'bin'
    if next_offset-offset>6:
      fileheader = original_data[offset:offset+4]
      if fileheader == b'\x89PNG':
        filetype = 'png'
      elif fileheader == b'"use':
        filetype = 'js'
      elif fileheader == b'RIFF':
        filetype = 'avi'
      elif fileheader == b'(fun':
        filetype = 'js'
      elif fileheader == b'<htm':
        filetype = 'htm'
      elif fileheader == b'<!DO':
        filetype = 'htm'
      elif fileheader == b'<!do':
        filetype = 'htm'
      elif original_data[offset:offset+2]==b'\x1f\x8b':
        filetype = 'gz'
    filew = original_data[offset:next_offset]
    if (filetype=='bin')and((filew.find(b'padding:')!=-1)or(filew.find(b'-webkit')!=-1)or(filew.find(b'margin:')!=-1)or(filew.find(b'width')!=-1)or(filew.find(b'styles')!=-1)or(filew.find(b'display')!=-1)or(filew.find(b'!important')!=-1)):
      filetype = 'css'
    if (filew.find(b'function')!=-1):
      filetype = 'js'
    of = open('Unpack\{0}.{1}'.format(id,filetype),'wb')
    of.write(filew)
    of.close()
def main():
  if len(sys.argv) > 1:
    os.chdir(sys.path[0])
    UnpackDataPack(sys.argv[1])
if __name__ == '__main__':
  main()