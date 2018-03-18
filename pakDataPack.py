from pakPackLib import WritePak,UniFile,Encodings,GetEncodingId
import sys
import os

def PakDataPack(file):
    oriFile=file[:file.rfind('_')]
    oriFilePos=oriFile.rfind('_')
    encoding=GetEncodingId(oriFile[oriFilePos+1:])
    oriFile=oriFile[:oriFilePos]+'.pak'
    resources={}
    for name in os.listdir(file):
        full=os.path.join(file,name)
        if(os.path.isfile(full)):
            inFile=open(full,'rb')
            resources[int(name)]=inFile.read()
            inFile.close()
    WritePak(UniFile(oriFile),resources,encoding)

def main():
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            PakDataPack(arg)

if __name__=='__main__':
    main()