import Server_Get_file_attr
import Server_Monitor
import Server_Read_file
import Server_Write_file
import Data_process
from enum import Enum

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

# build connection with client
# -------------need to implement----------------

# receive request from client
# -------------need to implement----------------
# also need to get the address of the client
address = client_address # address of the client(string)

# unmashalling
request = Data_process.deserialize(request)
operation = request["operation"]
# request format: 
# Read request: {"requestId":Id(int),"operation":"read", "pathname":pathname(str), "offset":offset(int), "length":length(int)}
if operation == "read":
    flag = True
    if "requestId" in request: # at-most-once
        if address in HISTORY:
            if request["requestId"] in HISTORY[address]:
                # send the recoreded reply to client
                requestId = request["requestId"]
                flag = False
    if flag:
        pathname = request["pathname"]
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
# Write request: {"requestId":Id(int),"operation":"write", "pathname":pathname(str), "offset":offset(int), "data":data(str)}
elif operation == "write":
    flag = True
    if "requestId" in request: # at-most-once
        if address in HISTORY:
            if request["requestId"] in HISTORY[address]:
                # send the recoreded reply to client
                requestId = request["requestId"]
                flag = False
    if flag:
        pathname = request["pathname"]
        offset = request["offset"]
        data = request["data"]
        return_value = Server_Write_file.write_file(pathname, offset, data)
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
# Get file attribute request: {"requestId":Id(int),"operation":"get_file_attr", "pathname":pathname(str)}
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
        pathname = request["pathname"]
        return_value = Server_Get_file_attr.get_file_attr(pathname)
        t_mserver = return_value
# Register Monitor request: {"requestId":Id(int),"operation":"register_monitor", "pathname":pathname(str), "interval":t(int)}
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
        pathname = request["pathname"]
        interval = request["interval"]
        return_value = Server_Monitor.register_monitor(pathname, interval)
        isSuccess = return_value
else:
    print("Invalid operation") # invalid operation should be checked by client

# send response to client
# reponse format:
# Read response: {"isSuccess":isSuccess(bool), "content":content(str)}
if operation == "read":
    if flag:
        response = {"isSuccess":isSuccess, "content":content}
    else:
        response = HISTORY[address][requestId]
# Write response: {"isSuccess":isSuccess(bool), "content":content(str)}
# Notify clients: {"notification":content(str)}
elif operation == "write":
    if flag:
        response = {"isSuccess":isSuccess, "content":content}
        if alive_clients:
            notification = {"notification":content}
            # marshalling
            for client in alive_clients:
                # send notification to each client
                # -------------need to implement----------------
                pass
    else:
        response = HISTORY[address][requestId]
# Get file attribute response: {"T_mserver":t_mserver(int)}
elif operation == "get_file_attr":
    if flag:
        response = {"T_mserver":t_mserver}
    else:
        response = HISTORY[address][requestId]
# Register Monitor response: {"isSuccess":isSuccess(bool)}
elif operation == "register_monitor":
    if flag:
        response = {"isSuccess":isSuccess}
    else:
        response = HISTORY[address][requestId]

else:
    print("No reponse")
# marshalling
response = Data_process.serialize(response)

# send to client
# -------------need to implement----------------


