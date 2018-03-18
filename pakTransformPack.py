from pakPackLib import ReadPak,WritePakV4,WritePak,UniFile
import sys
import os

def pakTransformPack(file):
    resources,_,encoding,version=ReadPak(file,True,True)
    if version==4:
        newFile=UniFile(file[:file.rfind('.')]+'.v5.pak')
        print('Transform "'+file+'"(v4) to "'+newFile+'(v5).')
        WritePak(newFile,resources,encoding)
    elif version==5:
        newFile=UniFile(file[:file.rfind('.')]+'.v4.pak')
        print('Transform "'+file+'"(v5) to "'+newFile+'(v4).')
        WritePakV4(newFile,resources,encoding)
    #Other cases will raise error in ReadPak directly.

def main():
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            pakTransformPack(arg)

if __name__=='__main__':
    main()