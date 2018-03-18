from pakPackLib import UniFile,GetMd5
import sys
import os
import json

def PakResAddByMerge(file):
    jsonFile=os.path.join(os.path.dirname(sys.argv[0]),'pakResIds.json')
    inFile=open(jsonFile,'r')
    ids=json.load(inFile)
    inFile.close()
    inFile=open(file,'r')
    newIds=json.load(inFile)
    inFile.close()
    for name in newIds:
        ids[name]=os.path.relpath(newIds[name]).replace('\\','/')
    outFile=open(UniFile(jsonFile),'w')
    json.dump(ids,outFile,indent=4,ensure_ascii=False)
    outFile.close()

def main():
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            PakResAddByMerge(arg)

if __name__=='__main__':
    main()