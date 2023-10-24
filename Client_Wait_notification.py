import Client_GLOBAL
import Client_Caching
import Data_process
from datetime import datetime

def wait_for_notification():
    # wait for update notification from the server
    print("#"*40 + "Waiting update notification from the Server" + "#"*40)
    notification, _= Client_GLOBAL.CLIENT_SOCKET.recvfrom(10240)
    notification = bytes.decode(notification)
    notification = Data_process.deserialize(notification)
    file_name = notification["file name"]
    content = notification["file updated"]
    print("File %s has been updated" % file_name)
    print("New content is: %s" % content)
    curr_dt = datetime.now()
    curr_t = int(round(curr_dt.timestamp()))
    Client_Caching.update_cache(file_name, content, curr_t, -1, 0, -1) # cache the whole updated file, keep the t_mclient unchanged
