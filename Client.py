import Client_Read_file
import Client_Write_file
import Client_Register_Monitor
import Client_Get_file_attr
import socket

# -------------------------------------------------GLOBAL STATE: START------------------------------------------------
# freeshness interval
# Need to set by user!!!!!!!
FRESHNESS_INTERVAL = -1

# {pathname:{T_c:int, T_mclient:int, content:string}}
CACHE = {}

# -------------------------------------------------GLOBAL STATE: END---------------------------------------------------
#######################################################################################################################
# -------------------------------------------------INITIALIZE the CLIENT: START----------------------------------------

# implement at-least-once and at-most-once
# Need to set by user!!!!!!!
# at-least-once: set TIMEOUT, DO NOT set REQUEST_ID
# at-most-once: set TIMEOUT AND set REQUEST_ID
TIMEOUT = -1
REQUEST_ID = -1
MODE = "initial mode"
while MODE != "at-least-once" and MODE != "at-most-once" and MODE != "none":
    MODE = input("Please input mode (at-least-once or at-most-once or none): ")
    if MODE == "at-least-once":
        while TIMEOUT < 0:
            input_value = input("Please input timeout (seconds)(an integer greater than 0): ")
            try:
                input_value = int(input_value)
                if input_value > 0:
                    TIMEOUT = input_value
                else:
                    print("Invalid timeout")
            except ValueError:
                print("Invalid timeout")

    elif MODE == "at-most-once":
        while TIMEOUT < 0:
            input_value = input("Please input timeout (seconds)(an integer greater than 0): ")
            try:
                input_value = int(input_value)
                if input_value > 0:
                    TIMEOUT = input_value
                else:
                    print("Invalid timeout")
            except ValueError:
                print("Invalid timeout")
            REQUEST_ID = 0
    
    elif MODE == "none":
        continue

    else:
        print("Invalid mode")

while FRESHNESS_INTERVAL < 0:
    input_value = input("Please input freshness interval (seconds)(an integer greater than 0): ")
    try:
        FRESHNESS_INTERVAL = int(input_value)
    except ValueError:
        print("Invalid freshness interval")

# build connection with client
# -------------need to implement----------------
CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # something like this
if TIMEOUT > 0:
    CLIENT_SOCKET.settimeout(TIMEOUT)

SERVER_ADDRESS = ('localhost', 12345) # something like this

# -------------------------------------------------INITIALIZE the CLIENT: END------------------------------------------
#######################################################################################################################
# ---------------------------------------------RECEIVE and SEND the REQUEST: START-------------------------------------

# get operation and parameters from user
# -------------need to implement----------------
operation = input("Please input operation: ") # something like this

# send request to server
# request format: 
# Read option: "read"
# Read request: {"operation":"read", "pathname":pathname(str), "offset":offset(int), "length":length(int)}
if operation == "read":
    pathname = input("Please input pathname: ")
    offset = int(input("Please input offset: "))
    length = int(input("Please input length of read: "))
    Client_Read_file.read_file(pathname,offset,length)

# Write insert option: "write insert"
# Write insert request: {"operation":"write_insert", "pathname":pathname(str), "offset":offset(int), "data":data(str)}
elif operation == "write insert":
    pathname = input("Please input pathname: ")
    offset = int(input("Please input offset: "))
    data = input("Please input data: ")
    Client_Write_file.write_insert(pathname,offset,data)

# Non-idempotent operation
# Write append option: "write append"
# Write append request: {"operation":"write_append", "pathname":pathname(str), "data":data(str)}
elif operation == "write append":
    pathname = input("Please input pathname: ")
    data = input("Please input data: ")
    Client_Write_file.write_append(pathname,data)

# Register Monitor option: "register monitor"
# Register Monitor request: {"operation":operation(str), "pathname":pathname(str), "interval":t(int)}
elif operation == "register monitor":
    pathname = input("Please input pathname: ")
    interval = int(input("Please input interval: "))
    Client_Register_Monitor.register_monitor(pathname,interval)

# Idempotent operation
# Get file attribute option: "get file attribute"
# Get file attribute request: {"operation":operation(str), "pathname":pathname(str)}
elif operation == "get file attribute":
    pathname = input("Please input pathname: ")
    # return format: (t_mserver(int), length(int)) (tuple)
    return_value = Client_Get_file_attr.get_file_attr(pathname)
    t_mserver = return_value[0]
    length = return_value[1]
    print("Last modifed time of %s on the server is %d" % (pathname, t_mserver))
    print("Length of %s is %d" % (pathname, length))

else:
    print("Invalid operation")

# receive response from server done in Client_Send_and_Receive.py and specific operation file
# ---------------------------------------------RECEIVE and SEND the REQUEST: END-------------------------------------