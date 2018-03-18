import collections
import os
import struct
import hashlib

BINARY,UTF8,UTF16=range(3)#type of encoding
Encodings=['BINARY','UTF-8','UTF-16']

class WrongFileVersion(Exception):
    pass

class NoRightsToAccess(Exception):
    pass

def GetEncodingId(encodingName):
    encoding=1
    idx=0
    for enc in Encodings:
        if enc==encodingName:
            encoding=idx
        idx+=1
    return encoding

def GetMd5(content):
    return hashlib.md5(content).hexdigest()

def ReadPakFromString(data,allResource=False,hasVersion=False):
    version=struct.unpack('<I',data[:4])[0]
    if version==4:
        resource_count,encoding=struct.unpack('<IB',data[4:9])
        alias_count=0
        header_size=9
    elif version==5:
        encoding,resource_count,alias_count=struct.unpack('<BxxxHH',data[4:12])
        header_size=12
    else:
        raise WrongFileVersion('Found unknown version: '+str(version)+'.')
    resources={}
    kIndexEntrySize=2+4#Each entry is a uint16 and a uint32.
    def entry_at_index(idx):
        offset=header_size+idx*kIndexEntrySize
        return struct.unpack('<HI',data[offset:offset+kIndexEntrySize])
    prev_resource_id,prev_offset=entry_at_index(0)
    for i in range(1,resource_count+1):
        resource_id,offset=entry_at_index(i)
        resources[prev_resource_id]=data[prev_offset:offset]
        prev_resource_id,prev_offset=resource_id,offset
    id_table_size = (resource_count + 1) * kIndexEntrySize
    kAliasEntrySize=2+2#uint16, uint16
    def alias_at_index(idx):
        offset=header_size+id_table_size+idx*kAliasEntrySize
        return struct.unpack('<HH',data[offset:offset+kAliasEntrySize])
    aliases={}
    for i in range(alias_count):
        resource_id,index=alias_at_index(i)
        aliased_id=entry_at_index(index)[0]
        aliases[resource_id]=aliased_id
        if allResource:
            resources[resource_id]=resources[aliased_id]
    if hasVersion:
        return resources,aliases,encoding,version
    else:
        return resources,aliases,encoding

def ReadPak(file,allResource=False,hasVersion=False):
    handler=open(file,'rb')
    ret=ReadPakFromString(handler.read(),allResource,hasVersion)
    handler.close()
    return ret

def WritePakToStringV4(resources,encoding):
    ret=[]
    resource_count=len(resources)
    ret.append(struct.pack('<IIB',4,resource_count,encoding))
    HEADER_LENGTH=9
    data_offset=HEADER_LENGTH+(resource_count+1)*6
    for resource_id in resources:#write table
        data=resources[resource_id]
        ret.append(struct.pack('<HI',resource_id,data_offset))
        data_offset+=len(data)
    ret.append(struct.pack('<HI', 0, data_offset))
    ret.extend(resources.values())#write data
    return b''.join(ret)

def WritePakV4(file,resources,encoding):
    content=WritePakToStringV4(resources,encoding)
    handler=open(file,'wb')
    handler.write(content)
    handler.close()

def WritePakToString(resources,encoding):
    ret=[]
    resource_ids=sorted(resources)#rebuild alias
    id_by_data={resources[k]: k for k in reversed(resource_ids)}
    alias_map = {k: id_by_data[v] for k, v in resources.items() if id_by_data[v] != k}
    resource_count=len(resources)-len(alias_map)#write head
    ret.append(struct.pack('<IBxxxHH',5,encoding,resource_count,len(alias_map)))
    HEADER_LENGTH=4+4+2+2
    data_offset=HEADER_LENGTH+(resource_count+1)*6+len(alias_map)*4
    index_by_id={}#write table
    deduped_data=[]
    index=0
    for resource_id in resource_ids:
        if resource_id in alias_map:
            continue
        data=resources[resource_id]
        index_by_id[resource_id]=index
        ret.append(struct.pack('<HI',resource_id,data_offset))
        data_offset+=len(data)
        deduped_data.append(data)
        index+=1
    ret.append(struct.pack('<HI', 0, data_offset))
    for resource_id in sorted(alias_map):#write alias table
        index=index_by_id[alias_map[resource_id]]
        ret.append(struct.pack('<HH', resource_id, index))
    ret.extend(deduped_data)#write data
    return b''.join(ret)

def WritePak(file,resources,encoding):
    content=WritePakToString(resources,encoding)
    handler=open(file,'wb')
    handler.write(content)
    handler.close()

def UniFile(file):#Ensure no file named as file(delete others or rename self)
    file=os.path.abspath(file)
    os.makedirs(os.path.dirname(file),exist_ok=True)
    if os.path.exists(file):
        dotIndex=file.rfind('.')
        if dotIndex!=-1:
            fileNoExt=file[:dotIndex]+' ('
            fileExt=')'+file[dotIndex:]
        else:
            fileNoExt=file+' ('
            fileExt=')'
        id=2
        renamedFile=fileNoExt+str(id)+fileExt
        while os.path.exists(renamedFile):
            id+=1
            renamedFile=fileNoExt+str(id)+fileExt
        if os.access(file,os.W_OK):
            os.rename(file,renamedFile)
            return file
        else:
            print('"'+file+'" cannot be written by this program, so we save it as '+renamedFile+'".')
            return renamedFile
    else:
        return file
