import Server_Write_file
import Client_Caching
from datetime import datetime

def write_file(pathname,offset,data):
    # marshalling
    # send operation and parameters to server
    # receive response from server
    # unmarshalling
    
    # if isSuccess is false, content is error message
    # if isSuccess is true, content is new file content
    # reponse format: {"isSuccess":isSuccess(bool), "content":content(str)}
    isSuccess, content = Server_Write_file.write_file(pathname,offset,data) # for test
    if isSuccess:
        curr_dt = datetime.now()
        curr_t = int(round(curr_dt.timestamp()))
        Client_Caching.update_cache(pathname,content,curr_t,curr_t)
        print(content)
        return True
    else:
        print(content) # Print error message
        return False

