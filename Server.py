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

# build connection with client
# -------------need to implement----------------

# receive request from client
# -------------need to implement----------------

# unmashalling
request = Data_process.deserialize(request)
operation = request["operation"]
# request format: 
# Read request: {"operation":operation(str), "pathname":pathname(str), "offset":offset(int), "length":length(int)}
if operation == "read":
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
# Write request: {"operation":operation(str), "pathname":pathname(str), "offset":offset(int), "data":data(str)}
elif operation == "write":
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
# Get file attribute request: {"operation":operation(str), "pathname":pathname(str)}
# Lack of error message
elif operation == "get_file_attr":
    pathname = request["pathname"]
    return_value = Server_Get_file_attr.get_file_attr(pathname)
    t_mserver = return_value
# Register Monitor request: {"operation":operation(str), "pathname":pathname(str), "interval":t(int)}
# Lack of error message
elif operation == "register_monitor":
    pathname = request["pathname"]
    interval = request["interval"]
    return_value = Server_Monitor.register_monitor(pathname, interval)
    isSuccess = return_value
else:
    print("Invalid operation")

# send response to client
# reponse format:
# Read response: {"isSuccess":isSuccess(bool), "content":content(str)}
if operation == "read":
    response = {"isSuccess":isSuccess, "content":content}
# Write response: {"isSuccess":isSuccess(bool), "content":content(str)}
# Notify clients: {"notification":content(str)}
elif operation == "write":
    response = {"isSuccess":isSuccess, "content":content}
    if alive_clients:
        notification = {"notification":content}
        # marshalling
        for client in alive_clients:
            # send notification to each client
            # -------------need to implement----------------
            pass
# Get file attribute response: {"T_mserver":t_mserver(int)}
elif operation == "get_file_attr":
    response = {"T_mserver":t_mserver}
# Register Monitor response: {"isSuccess":isSuccess(bool)}
elif operation == "register_monitor":
    response = {"isSuccess":isSuccess}

# marshalling
response = Data_process.serialize(response)

# send to client
# -------------need to implement----------------


