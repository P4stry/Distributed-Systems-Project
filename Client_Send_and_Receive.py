import Client
import Data_process
from datetime import datetime
# input: socket, request(dictionary)
# marshalling
# send operation and parameters to server
# receive response from server
# unmarshalling
# return dictoinary to called function

def send_and_receive(request):
    # at-most-once
    if Client.REQUEST_ID != -1:
        request["requestId"] = Client.REQUEST_ID
        Client.REQUEST_ID += 1
    # marshalling
    request = Data_process.serialize(request)
    # send request(str) to server
    # -------------need to implement----------------
    Client.CLIENT_SOCKET.sendto(request,Client.SERVER_ADDRESS) # something like this
    
    # repeatly send if no respond within timeout (curr_t - last_send_t > Client.TIMEOUT)
    # -------------need to implement----------------
    # record send time
    curr_dt = datetime.now() # something like this
    last_send_t = int(round(curr_dt.timestamp())) # something like this
    # -------------need to implement----------------

    # receive response(str) from server
    # -------------need to implement----------------
    response = Client.CLIENT_SOCKET.recvfrom(1024) # something like this

    # unmarshalling
    response = Data_process.deserialize(response)
    return response