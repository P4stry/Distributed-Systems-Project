import Client_Caching
import Client_Send_and_Receive
from datetime import datetime

def write_file(pathname,offset,data):
    # if isSuccess is false, content is error message
    # if isSuccess is true, content is new file content
    # reponse format: {"isSuccess":isSuccess(bool), "content":content(str)}
    request = {"operation":"write", "pathname":pathname, "offset":offset, "data":data}
    response = Client_Send_and_Receive.send_and_receive(request)
    isSuccess = response["isSuccess"]
    content = response["content"]
    if isSuccess:
        curr_dt = datetime.now()
        curr_t = int(round(curr_dt.timestamp()))
        Client_Caching.update_cache(pathname,content,curr_t,curr_t)
        print(content)
        return True
    else:
        print(content) # Print error message
        return False

