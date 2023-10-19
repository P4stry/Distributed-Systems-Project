import Client_Caching
import Server_Read_file
from datetime import datetime

def read_file(pathname,offset,length):
    isValid = Client_Caching.check_cache(pathname)
    if isValid:
        content = Client_Caching.read_from_cache(pathname,offset,length)
    else:
        # marshalling
        # send operation and parameters to server
        # receive response from server
        # unmarshalling

        # if isSuccess is false, content is error message
        # if isSuccess is true, content is file content
        # reponse format: {"isSuccess":isSuccess(bool), "content":content(str)}
        isSuccess, content = Server_Read_file.read_file(pathname,offset,length) # for test
        if isSuccess:
            curr_dt = datetime.now()
            curr_t = int(round(curr_dt.timestamp()))
            Client_Caching.update_cache(pathname,content,curr_t,-1)
        else:
            print(content)
            return False
    print(content)
    return True