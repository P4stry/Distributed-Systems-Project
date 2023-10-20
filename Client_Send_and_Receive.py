import Client
import Data_process
from datetime import datetime
import random
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

    # Timeout senario
    # -------------need to implement----------------
    if Client.TIMEOUT > 0:
        # record receive reponse or not
        flag = False
        while not flag:
            # send request(str) to server
            # -------------need to implement----------------
            Client.CLIENT_SOCKET.sendto(request,Client.SERVER_ADDRESS) # something like this
            # receive response
            try:
                # receive response(str) from server
                # -------------need to implement----------------
                response = Client.CLIENT_SOCKET.recvfrom(1024) # something like this
                flag = True
            except Client.CLIENT_SOCKET.timeout:
                print("Timeout, no response from server within %d seconds" % Client.TIMEOUT)
                print("Resend request")
                continue
    # No timeout senario
    else:
        # send request(str) to server
        # -------------need to implement----------------
        Client.CLIENT_SOCKET.sendto(request,Client.SERVER_ADDRESS) # something like this
        # receive response(str) from server
        # -------------need to implement----------------
        response = Client.CLIENT_SOCKET.recvfrom(1024) # something like this

    # unmarshalling
    response = Data_process.deserialize(response)
    return response