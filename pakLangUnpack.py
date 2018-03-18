from pakPackLib import ReadPak,Encodings,UniFile
import sys
import json
import os

def PakLangUnpack(file):
    resources,aliases,encoding=ReadPak(file)
    merged={}
    for id in resources:
        merged[id]={'ids':[id],'text':resources[id].decode(Encodings[encoding])}
    for id in aliases:
        merged[aliases[id]]['ids'].append(id)
    listed=list(merged.values())
    listed.insert(0,{'encoding':Encodings[encoding]})
    outFile=open(UniFile(file[:file.rfind('.')]+'.json'),'w',encoding=Encodings[encoding])
    json.dump(listed,outFile,indent=4,ensure_ascii=False)
    outFile.close()

def main():
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            PakLangUnpack(arg)

if __name__=='__main__':
    main()