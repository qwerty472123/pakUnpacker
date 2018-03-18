from pakPackLib import WritePak,UniFile,Encodings,GetEncodingId
import sys
import json
import os

def PakLangPack(file):
    prencoding='UTF-8'
    inFile=open(file,'r',encoding=prencoding)
    content=json.load(inFile)
    inFile.close()
    encoding=content[0]['encoding']
    iencoding=GetEncodingId(encoding)
    if encoding!=prencoding:
        inFile=open(file,'r',encoding=encoding)
        content=json.load(inFile)
        inFile.close()
    resources={}
    content=content[1:]
    for info in content:
        data=info["text"].encode(encoding)
        for idx in info['ids']:
            resources[int(idx)]=data
    WritePak(UniFile(file[:file.rfind('.')]+'.pak'),resources,iencoding)

def main():
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            PakLangPack(arg)

if __name__=='__main__':
    main()