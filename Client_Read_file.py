import Client_Caching
import Client_Send_and_Receive
from datetime import datetime

def read_file(pathname,offset,length):
    isValid = Client_Caching.check_cache(pathname, offset, length)
    if isValid:
        print("Read from cache")
        content = Client_Caching.read_from_cache(pathname,offset,length)
    else:
        # if isSuccess is false, content is error message
        # if isSuccess is true, content is file content
        # reponse format: {"isSuccess":isSuccess(bool), "content":content(str)}
        request = {"operation":"read", "pathname":pathname, "offset":offset, "length":length}
        response = Client_Send_and_Receive.send_and_receive(request)
        isSuccess = response["isSuccess"]
        content = response["content"]
        if isSuccess:
            curr_dt = datetime.now()
            curr_t = int(round(curr_dt.timestamp()))
            Client_Caching.update_cache(pathname, content, curr_t, -1, offset, length)
        else:
            print(content)
            return False
    print(content)
    return True