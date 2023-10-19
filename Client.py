import Client_Caching
import Client_Read_file
import Client_Write_file
import Client_Register_Monitor
import Data_process

FRESHNESS_INTERVAL = 0

# {pathname:{T_c:int, T_mclient:int, content:string}}
CACHE = {}

# build connection with client
# -------------need to implement----------------

# get operation and parameters from user
# -------------need to implement----------------
operation = input("Please input operation: ") # something like this

# send request to server
# request format: 
# Read request: {"operation":operation(str), "pathname":pathname(str), "offset":offset(int), "length":length(int)}
if operation == "read":
    pathname = input("Please input pathname: ")
    offset = int(input("Please input offset: "))
    length = int(input("Please input length of read: "))
    request = {"operation":operation, "pathname":pathname, "offset":offset, "length":length}
# Write request: {"operation":operation(str), "pathname":pathname(str), "offset":offset(int), "data":data(str)}
elif operation == "write":
    pathname = input("Please input pathname: ")
    offset = int(input("Please input offset: "))
    data = input("Please input data: ")
    request = {"operation":operation, "pathname":pathname, "offset":offset, "data":data}
# Get file attribute request: {"operation":operation(str), "pathname":pathname(str)}

# Register Monitor request: {"operation":operation(str), "pathname":pathname(str), "interval":t(int)}
elif operation == "register monitor":
    pathname = input("Please input pathname: ")
    interval = int(input("Please input interval: "))
    request = {"operation":operation, "pathname":pathname, "interval":interval}
# marshalling
request = Data_process.serialize(request)
# send request to server

# receive response from server
# unmarshalling
# reponse format:
# Read response: {"isSuccess":isSuccess(bool), "content":content(str)}
# Write response: {"isSuccess":isSuccess(bool), "content":content(str)}
# Get file attribute response: {"T_mserver":t_mserver(int)}
# Register Monitor response: {"isSuccess":isSuccess(bool)}