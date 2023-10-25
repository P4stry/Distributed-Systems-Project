import Client_GLOBAL
import Client_Caching
import Data_process
from datetime import datetime
from socket import timeout

def wait_for_notification(interval):
    curr_dt = datetime.now()
    curr_t = int(round(curr_dt.timestamp()))
    expiration = curr_t + interval
    Client_GLOBAL.CLIENT_SOCKET.settimeout(interval)

    # for test
    # print("Start time is %d" % curr_t)
    
    while expiration > curr_t:
        # wait for update notification from the server
        print("#"*40 + "Waiting update notification from the Server" + "#"*40)
        try:
            notification, _= Client_GLOBAL.CLIENT_SOCKET.recvfrom(10240)
        except timeout:
            print("The monitoring interval expired, exit monitoring")
            break
        notification = bytes.decode(notification)
        notification = Data_process.deserialize(notification)
        file_name = notification["file name"]
        content = notification["file updated"]
        print("File %s has been updated" % file_name)
        print("New content is: %s" % content)
        
        #record the update
        curr_dt = datetime.now()
        curr_t = int(round(curr_dt.timestamp()))
        Client_Caching.update_cache(file_name, content, curr_t, -1, 0, -1) # cache the whole updated file, keep the t_mclient unchanged
        
        # update timeout
        Client_GLOBAL.CLIENT_SOCKET.settimeout(expiration - curr_t)

    # for test
    # curr_dt = datetime.now()
    # curr_t = int(round(curr_dt.timestamp()))
    # print("End time is %d" % curr_t)
    
    # reset timeout !!!!!!!!!!!!!
    if Client_GLOBAL.TIMEOUT > 0:
        Client_GLOBAL.CLIENT_SOCKET.settimeout(Client_GLOBAL.TIMEOUT)
    else:
        Client_GLOBAL.CLIENT_SOCKET.settimeout(None)
