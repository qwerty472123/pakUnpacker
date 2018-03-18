from pakPackLib import UniFile,GetMd5
import sys
import os
import json

def PakResAddByDir(file):
    jsonFile=os.path.join(os.path.dirname(sys.argv[0]),'pakResIds.json')
    inFile=open(jsonFile,'r')
    ids=json.load(inFile)
    inFile.close()
    for root,_,files in os.walk(file):
        for name in files:
            full=os.path.abspath(os.path.join(root,name))
            absName=os.path.relpath(full,file)
            if not(absName.startswith('unknown\\')or absName.startswith('preAlias\\')or absName.startswith('alias\\')):
                inFile=open(full,'rb')
                ids[GetMd5(inFile.read())]=absName.replace('\\','/')
                inFile.close()
    outFile=open(UniFile(jsonFile),'w')
    json.dump(ids,outFile,indent=4,ensure_ascii=False)
    outFile.close()

def main():
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            PakResAddByDir(arg)

if __name__=='__main__':
    main()