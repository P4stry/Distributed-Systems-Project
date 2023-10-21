import Server_Get_file_attr
import Server_Monitor
import Server_Read_file
import Server_Write_file
import Server_Get_file_list
import Data_process
import socket
from enum import Enum
import time
import random

# -------------------------------------------------GLOBAL STATE: START------------------------------------------------

class Error(Enum):
    FILE_OPEN_ERROR = 0
    FILE_SEEK_ERROR = 1

# {pathname(str):t(int)}
FILE_ATTR = {}

# {pathname(str):{address(str):expiration(int)(sec)}}
# MONITORING = {"test.txt":{"192.168.0.1":1797625518, "192.168.0.2":1597625518}}
MONITORING = {}

# log requests and replies history
# {address(str):{requestId(int):reply(str)}}
HISTORY = {}

# -------------------------------------------------GLOBAL STATE: END---------------------------------------------------
#######################################################################################################################
# -------------------------------------------------INITIALIZE the SERVER: START----------------------------------------

# for at-most-once and at-least-once and message loss test
# Need to set by user!!!!!!!
SLEEP_INTERVAL = -1
TEST_LOSS = False

while True:
    choose = input("Test timeout? (y/n): ")
    if choose == "y":
        while SLEEP_INTERVAL < 0:
            input_value = input("Please input sleep interval (seconds)(an integer greater than 0): ")
            try: # check integer
                input_value = int(input_value)
                if input_value > 0: # check greater than 0
                    SLEEP_INTERVAL = input_value
                else:
                    print("Invalid sleep interval")
            except ValueError:
                print("Invalid sleep interval")
        break
    elif choose == "n":
        # SLEEP_INTERVAL = -1
        break
    else:
        print("Invalid input")

while True:
    choose = input("Test message loss? (y/n): ")
    if choose == "y":
        TEST_LOSS = True
        break
    elif choose == "n":
        # TEST_LOSS = False
        break
    else:
        print("Invalid input")

# build connection with client
# -------------need to implement----------------
# something like this
SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SERVER_ADDRESS = ('localhost', 12345)
SERVER_SOCKET.bind(SERVER_ADDRESS)

# -------------------------------------------------INITIALIZE the SERVER: END------------------------------------------
#######################################################################################################################
# ---------------------------------------------RECEIVE and HANDLE the REQUEST: START-----------------------------------

while True:
    print("Waiting for client")
    # receive request from client
    # -------------need to implement----------------
    # also need to get the address of the client
    request, client_address= SERVER_SOCKET.recvfrom(1024)
    address = client_address[0] + ":" + str(client_address[1]) # convert (client_ip(str),client_port(int)) to the address(string), format: "ip:port"

    # unmashalling
    request = Data_process.deserialize(request)
    operation = request["operation"]

    # request format:
    # List files request: {"requestId":Id(int),"operation":"list_files"} at-most-once
    # List files request: {"operation":"list_files"} at-least-once
    if operation == "list_files":
        flag = True
        if "requestId" in request:
            if address in HISTORY:
                if request["requestId"] in HISTORY[address]:
                    # send the recoreded reply to client
                    requestId = request["requestId"]
                    flag = False
        if flag:
            return_value = Server_Get_file_list.get_file_list()

    # Read request: {"requestId":Id(int),"operation":"read", "pathname":pathname(str), "offset":offset(int), "length":length(int)} at-most-once
    # Read request: {"operation":"read", "pathname":pathname(str), "offset":offset(int), "length":length(int)} at-least-once
    elif operation == "read":
        flag = True
        if "requestId" in request: # at-most-once
            if address in HISTORY:
                if request["requestId"] in HISTORY[address]:
                    # send the recoreded reply to client
                    requestId = request["requestId"]
                    flag = False
        if flag:
            pathname = 'Shared file/' + request["pathname"]
            offset = request["offset"]
            length = request["length"]
            return_value = Server_Read_file.read_file(pathname,offset,length)
            if return_value == Error.FILE_OPEN_ERROR:
                isSuccess = False
                content = "Cannot open file, please check the pathname"
            elif return_value == Error.FILE_SEEK_ERROR:
                isSuccess = False
                content = "Offset exceeds the file length"
            else:
                isSuccess = True
                content = return_value

    # Write insert request: {"requestId":Id(int),"operation":"write_insert", "pathname":pathname(str), "offset":offset(int), "data":data(str)} at-most-once
    # Write insert request: {"operation":"write_insert", "pathname":pathname(str), "offset":offset(int), "data":data(str)} at-least-once
    elif operation == "write_insert":
        flag = True
        if "requestId" in request: # at-most-once
            if address in HISTORY:
                if request["requestId"] in HISTORY[address]:
                    # send the recoreded reply to client
                    requestId = request["requestId"]
                    flag = False
        if flag:
            pathname = 'Shared file/' + request["pathname"]
            offset = request["offset"]
            data = request["data"]
            return_value = Server_Write_file.write_insert(pathname, offset, data)
            if return_value == Error.FILE_OPEN_ERROR:
                isSuccess = False
                content = "Cannot open file, please check the pathname"
            elif return_value == Error.FILE_SEEK_ERROR:
                isSuccess = False
                content = "Offset exceeds the file length"
            else:
                isSuccess = True
                alive_clients = return_value[1]
                content = return_value[2]

    # Non-idempotent
    # Write append request: {"requestId":Id(int),"operation":"write_append", "pathname":pathname(str), "data":data(str)} at-most-once
    # Write append request: {"operation":"write_append", "pathname":pathname(str), "data":data(str)} at-least-once
    elif operation == "write_append":
        flag = True
        if "requestId" in request:
            if address in HISTORY:
                if request["requestId"] in HISTORY[address]:
                    # send the recoreded reply to client
                    requestId = request["requestId"]
                    flag = False
        if flag:
            pathname = 'Shared file/' + request["pathname"]
            data = request["data"]
            return_value = Server_Write_file.write_append(pathname, data)
            if return_value == Error.FILE_OPEN_ERROR:
                isSuccess = False
                content = "Cannot open file, please check the pathname"
            else:
                isSuccess = True
                alive_clients = return_value[1]
                content = return_value[2]

    # Idempotent
    # Get file attribute request: {"requestId":Id(int),"operation":"get_file_attr", "pathname":pathname(str)} at-most-once
    # Get file attribute request: {"operation":"get_file_attr", "pathname":pathname(str)} at-least-once
    # Lack of error message
    elif operation == "get_file_attr":
        flag = True
        if "requestId" in request: # at-most-once
            if address in HISTORY:
                if request["requestId"] in HISTORY[address]:
                    # send the recoreded reply to client
                    requestId = request["requestId"]
                    flag = False
        if flag:
            pathname = 'Shared file/' + request["pathname"]
            return_value = Server_Get_file_attr.get_file_attr(pathname)
            t_mserver = return_value[0]
            length = return_value[1]

    # Register Monitor request: {"requestId":Id(int),"operation":"register_monitor", "pathname":pathname(str), "interval":t(int)} at-most-once
    # Register Monitor request: {"operation":"register_monitor", "pathname":pathname(str), "interval":t(int)} at-least-once
    # Lack of error message
    elif operation == "register_monitor":
        flag = True
        if "requestId" in request: # at-most-once
            if address in HISTORY:
                if request["requestId"] in HISTORY[address]:
                    # send the recoreded reply to client
                    requestId = request["requestId"]
                    flag = False
        if flag:
            pathname = 'Shared file/' + request["pathname"]
            interval = request["interval"]
            return_value = Server_Monitor.register(pathname, address, interval)
            isSuccess = return_value

    else:
        print("Invalid operation") # invalid operation should be checked by client

    # ---------------------------------------------RECEIVE and HANDLE the REQUEST: END-------------------------------------
    #######################################################################################################################
    # ------------------------------------------------SEND RESPONSE to the CLIENT: START-----------------------------------

    # Send response to client
    # reponse format:
    # List files response: {"file_list":file_list(list)}
    if operation == "list_files":
        if flag:
            response = {"file_list":return_value}
            # record the reply, if at-most-once
            if "requestId" in request:
                requestId = request["requestId"]
                HISTORY[address] = {requestId:response}
        else:
            response = HISTORY[address][requestId]

    # Read response: {"isSuccess":isSuccess(bool), "content":content(str)}
    elif operation == "read":
        if flag:
            response = {"isSuccess":isSuccess, "content":content}
            # record the reply, if at-most-once
            if "requestId" in request:
                requestId = request["requestId"]
                HISTORY[address] = {requestId:response}
        else:
            response = HISTORY[address][requestId]

    # Write response: {"isSuccess":isSuccess(bool), "content":content(str)}
    # Notify clients: {"notification":content(str)}
    elif operation == "write":
        if flag:
            response = {"isSuccess":isSuccess, "content":content}
            # record the reply, if at-most-once
            if "requestId" in request:
                requestId = request["requestId"]
                HISTORY[address] = {requestId:response}

            # notify other clients
            if alive_clients:
                notification = {"file name": request["pathname"], "file updated":content}
                # marshalling
                notification = Data_process.serialize(notification)
                for alive_client in alive_clients:
                    # conver "ip:port" to (ip(str),port(int))(tuple)
                    address_ip = alive_client.split(":")
                    alive_client_address = (address_ip[0],int(address_ip[1]))
                    # send notification to each client
                    SERVER_SOCKET.sendto(response,alive_client_address)
        else:
            response = HISTORY[address][requestId]

    # Get file attribute response: {"T_mserver":t_mserver(int), "length":length(int)}
    elif operation == "get_file_attr":
        if flag:
            response = {"T_mserver":t_mserver, "length":length}
            # record the reply, if at-most-once
            if "requestId" in request:
                requestId = request["requestId"]
                HISTORY[address] = {requestId:response}
        else:
            response = HISTORY[address][requestId]

    # Register Monitor response: {"isSuccess":isSuccess(bool)}
    elif operation == "register_monitor":
        if flag:
            response = {"isSuccess":isSuccess}
            # record the reply, if at-most-once
            if "requestId" in request:
                requestId = request["requestId"]
                HISTORY[address] = {requestId:response}
        else:
            response = HISTORY[address][requestId]

    else:
        print("No reponse")
    # marshalling
    response = Data_process.serialize(response)

    # send to client
    # -------------need to implement----------------
    # test timeout
    if SLEEP_INTERVAL > 0:
        time.sleep(SLEEP_INTERVAL)

    # test message loss
    if TEST_LOSS:
        loss = random.randint(0,1)
        if loss == 1:
            SERVER_SOCKET.sendto(response,client_address) # something like this

    SERVER_SOCKET.sendto(response,client_address) # something like this

    # ------------------------------------------------SEND RESPONSE to the CLIENT: END-----------------------------------------------

