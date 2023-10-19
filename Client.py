import Client_Read_file
import Client_Write_file
import Client_Register_Monitor
import socket

FRESHNESS_INTERVAL = 0

# {pathname:{T_c:int, T_mclient:int, content:string}}
CACHE = {}

# implement at-least-once and at-most-once
# at-least-once: set TIMEOUT, DO NOT set REQUEST_ID
# at-most-once: set TIMEOUT AND set REQUEST_ID
TIMEOUT = -1
REQUEST_ID = -1

# build connection with client
# -------------need to implement----------------
CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # something like this
SERVER_ADDRESS = ('localhost', 12345) # something like this
# get socket

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
    Client_Read_file.read_file(pathname,offset,length)

# Write request: {"operation":operation(str), "pathname":pathname(str), "offset":offset(int), "data":data(str)}
elif operation == "write":
    pathname = input("Please input pathname: ")
    offset = int(input("Please input offset: "))
    data = input("Please input data: ")
    Client_Write_file.write_file(pathname,offset,data)

# Get file attribute request: {"operation":operation(str), "pathname":pathname(str)}
# -------------need to implement----------------

# Register Monitor request: {"operation":operation(str), "pathname":pathname(str), "interval":t(int)}
elif operation == "register monitor":
    pathname = input("Please input pathname: ")
    interval = int(input("Please input interval: "))
    Client_Register_Monitor.register_monitor(pathname,interval)

else:
    print("Invalid operation")

# receive response from server done in Client_Send_and_Receive.py and specific operation file