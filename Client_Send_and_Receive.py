import Client_GLOBAL
import Data_process
from socket import timeout
import time
import random
# marshalling
# send operation and parameters to server
# receive response from server
# unmarshalling
# return dictoinary to called function

def send_and_receive(request):
    # at-most-once
    if Client_GLOBAL.REQUEST_ID != -1:
        request["requestId"] = Client_GLOBAL.REQUEST_ID
        Client_GLOBAL.REQUEST_ID += 1
    # marshalling
    request = Data_process.serialize(request)

    # Timeout senario
    if Client_GLOBAL.TIMEOUT > 0:

        # maybe have better way to empty the buffer of socket
        print("-"*35 + "Emptying the buffer of socket, please wait" + "-"*35)
        time.sleep(Client_GLOBAL.TIMEOUT + 1)
        while True:
            try:
                _ = Client_GLOBAL.CLIENT_SOCKET.recvfrom(1024)
            except:
                break
        print("-"*50 + "Emptying end" + "-"*50)

        # record receive reponse or not
        flag = False
        while not flag:
            # test message loss
            if Client_GLOBAL.TEST_LOSS:
                success = random.randint(1,100)
                if success > Client_GLOBAL.POSSIBILITY_OF_LOSS:
                   Client_GLOBAL.CLIENT_SOCKET.sendto(str.encode(request),Client_GLOBAL.SERVER_ADDRESS)
                else:
                    print("Message loss")
            # send request(str) to server
            else:
                Client_GLOBAL.CLIENT_SOCKET.sendto(str.encode(request),Client_GLOBAL.SERVER_ADDRESS)
            # receive response
            try:
                # receive response(str) from server
                response, _= Client_GLOBAL.CLIENT_SOCKET.recvfrom(10240)
                flag = True
            except timeout:
                print("Timeout, no response from server within %d seconds" % Client_GLOBAL.TIMEOUT)
                print("Resend request")
                print("\\"*50 + "Retrying" + "/"*50)
                continue
        

    # No timeout senario
    else:
        # test message loss
        if Client_GLOBAL.TEST_LOSS:
            success = random.randint(1,100)
            if success > Client_GLOBAL.POSSIBILITY_OF_LOSS:
                Client_GLOBAL.CLIENT_SOCKET.sendto(str.encode(request),Client_GLOBAL.SERVER_ADDRESS)
            else:
                print("Message loss")
        # send request(str) to server
        else:
            Client_GLOBAL.CLIENT_SOCKET.sendto(str.encode(request),Client_GLOBAL.SERVER_ADDRESS)
        # receive response(str) from server
        response, _= Client_GLOBAL.CLIENT_SOCKET.recvfrom(10240)

    # unmarshalling
    response = bytes.decode(response)
    response = Data_process.deserialize(response)
    
    return response