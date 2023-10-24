from datetime import datetime
import Client_Get_file_attr
import Client_GLOBAL
'''
Description: 
The file content read by the client is retained in a buffer of the client program. 
If the file content requested by the client is available in the cache, 
the client may read the cached content directly without contacting the server. 
On the other hand, the updates made by the client to file content are always sent to the server immediately. 
The approximate one-copy update semantics (used by NFS as described in the lecture) is required to be implemented to maintain cache consistency.
Parameter: freshness interval t
Need to maintain some meta-information of cached content 
(e.g., the file pathname of the cached content, the time when the cached content was last validated).
In NFS
T_c: the time when the cache entry was last validated
T_mclient: the time when the cached file was last modified at server
T: current time
Entry is considered valid when T - T_c < t
T - T_c < t, no need to evaluate further, read data from cache
T - T_c ≥ t, issue getattr call to server to obtain T_mserver(update T_c)
    T_mclient = T_mserver, the cache entry is valid (the data have not been modified at the server) and T_c is updated to current time
    T_mclient < T_mserver, the cache entry is invalidated, and a new request is sent to server for updated data, T_c is also updated
'''
# CACHE = {pathname:{offset:int, end:int, T_c:int, T_mclient:int, content:string}}

def check_cache(pathname, offset, length):
    curr_dt = datetime.now()
    curr_t = int(round(curr_dt.timestamp()))
    if pathname in Client_GLOBAL.CACHE:
        # check if offset and length are valid
        # if end == -1, the whole file is cached (last cache is updated by write operation)
        if offset < Client_GLOBAL.CACHE[pathname]["offset"] or (offset + length - 1) > Client_GLOBAL.CACHE[pathname]["end"]:
            if Client_GLOBAL.CACHE[pathname]["end"] == -1:
                pass
            else:
                return False
        if curr_t - Client_GLOBAL.CACHE[pathname]["T_c"] < Client_GLOBAL.FRESHNESS_INTERVAL:
            return True
        else:
            # return format: (t_mserver(int), length(int)) (tuple)
            return_value = Client_Get_file_attr.get_file_attr(pathname)
            t_mserver = return_value[0]
            if Client_GLOBAL.CACHE[pathname]["T_mclient"] == t_mserver:
                Client_GLOBAL.CACHE[pathname]["T_c"] = curr_t
                return True
            else:
                return False
    else:
        return False

        
def read_from_cache(pathname,offset,length):
    # recaculate offset in cached content
    offset = offset - Client_GLOBAL.CACHE[pathname]["offset"]

    content = Client_GLOBAL.CACHE[pathname]["content"]
    return content[offset : offset + length]

def update_cache(pathname, data , t_c, t_mclient, offset, length):
    if pathname in Client_GLOBAL.CACHE:
        Client_GLOBAL.CACHE[pathname]["content"] = data
        Client_GLOBAL.CACHE[pathname]["T_c"] = t_c
        Client_GLOBAL.CACHE[pathname]["offset"] = offset
        if length == -1: # whole file is cached
            Client_GLOBAL.CACHE[pathname]["end"] = -1 # write operation updates
        else:
            Client_GLOBAL.CACHE[pathname]["end"] = offset + length - 1 # read operation updates
        if t_mclient != -1: # write operation updates
            Client_GLOBAL.CACHE[pathname]["T_mclient"] = t_mclient
    else:
        if length == -1: # write operation updates
            end = -1
        else:
            end = offset + length - 1 # read operation updates
        Client_GLOBAL.CACHE[pathname] = {"offset":offset, "end": end, "T_c":t_c, "T_mclient":t_mclient, "content":data}