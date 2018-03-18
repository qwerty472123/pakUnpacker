from pakPackLib import UniFile,GetMd5
import sys
import os
import json

def PakResLink(file,linkFull=False,linkAlias=False,hardLink=False):
    def link(src,dst):
        if hardLink:
            os.link(src,dst)
        else:
            os.symlink(src,dst)
    inFile=open(os.path.join(os.path.dirname(sys.argv[0]),'pakResIds.json'),'r')
    ids=json.load(inFile)
    inFile.close()
    dirname=UniFile(file[:file.rfind('_')]+'_link')
    os.mkdir(dirname)
    for name in os.listdir(file):
        full=os.path.abspath(os.path.join(file,name))
        inFile=open(full,'rb')
        content=inFile.read()
        inFile.close()
        def getUnknownName(type):
            ext=''
            if len(content)>6:
                head=content[:4]
                if head==b'\x89PNG':
                    ext='.png'
                elif head==b'"use':
                    ext='.js'
                elif head==b'RIFF':
                    ext='.avi'
                elif head==b'(fun':
                    ext='.js'
                elif head==b'<htm':
                    ext='.htm'
                elif head==b'<!DO' or head==b'<!do' or head==b'<!--':
                    ext='.htm'
                elif head[:2]==b'\x1f\x8b':
                    ext='.gz'
                elif content.find(b'function')!=-1:
                    ext='.js'
                elif head[:1]==b'{':
                    ext='.json'
                elif head[:1]==b'<':
                    ext='.htm'
                elif content.find(b'width')!=-1 or content.find(b'styles')!=-1 or content.find(b'display')!=-1 or content.find(b'!important')!=-1:
                    ext='.css'
            return UniFile(os.path.join(dirname,type,name+ext))
        if os.path.islink(full):
            if linkAlias:
                link(full,getUnknownName('alias'))
        else:
            md5=GetMd5(content)
            if md5 in ids:
                newName=os.path.join(dirname,ids[md5])
                if os.path.exists(newName):
                    if linkAlias:
                        print('"'+newName+'" has existed as a non alias file, save it to preAlias.')
                        link(full,getUnknownName('preAlias'))
                    else:
                        print('"'+newName+'" has existed as a non alias file, ignore it.')
                else:
                    link(full,UniFile(newName))
            else:
                if linkFull:
                    print(name+'('+md5+') is not in res list, save it to unknwon')
                    link(full,getUnknownName('unknown'))
                else:
                    print(name+'('+md5+') is not in res list, ignore it.')

def main():
    args=sys.argv[1:]
    linkFull=False
    linkAlias=False
    hardLink=False
    for arg in args:
        if arg=='-f':#link unknown files
            linkFull=True
        elif arg=='-a':#link alias and other same-name files
            linkAlias=True
        elif arg=='-h':#link file by hard link os.link
            hardLink=True
    for arg in sys.argv[1:]:
        if not arg.startswith('-') and os.path.isdir(arg):
            PakResLink(arg,linkFull,linkAlias,hardLink)

if __name__=='__main__':
    main()