from pakPackLib import ReadPak,Encodings,UniFile
import sys
import os

def PakDataUnpack(file,hardLink=False):
    resources,aliases,encoding=ReadPak(file)
    dirname=UniFile(file[:file.rfind('.')]+'_'+Encodings[encoding]+'_data')
    os.mkdir(dirname)
    for id in resources:
        outFile=open(os.path.join(dirname,str(id)),'wb')
        outFile.write(resources[id])
        outFile.close()
    if hardLink:
        for id in aliases:
            os.link(os.path.join(dirname,str(aliases[id])),os.path.join(dirname,str(id)))
    else:
        for id in aliases:
            os.symlink(os.path.join(dirname,str(aliases[id])),os.path.join(dirname,str(id)))

def main():
    args=sys.argv[1:]
    hardLink=False
    for arg in args:
        if arg=='-h':#link file by hard link os.link
            hardLink=True
    for arg in sys.argv[1:]:
        if not arg.startswith('-') and os.path.isfile(arg):
            PakDataUnpack(arg,hardLink)

if __name__=='__main__':
    main()