import Client_GLOBAL
import Client_Get_file_list
import Client_Read_file
import Client_Write_file
import Client_Register_Monitor
import Client_Get_file_attr
import Client_Wait_notification

#######################################################################################################################
# -------------------------------------------------INITIALIZE the CLIENT: START----------------------------------------

# implement at-least-once and at-most-once
# Need to set by user!!!!!!!
# at-least-once: set TIMEOUT, DO NOT set REQUEST_ID
# at-most-once: set TIMEOUT AND set REQUEST_ID
MODE = "initial mode"
while MODE != "at-least-once" and MODE != "at-most-once" and MODE != "none":
    MODE = input("Please input mode (at-least-once or at-most-once or none): ")
    if MODE == "at-least-once":
        while Client_GLOBAL.TIMEOUT < 0:
            input_value = input("Please input timeout (seconds)(an integer greater than 0): ")
            try:
                input_value = int(input_value)
                if input_value > 0:
                    Client_GLOBAL.TIMEOUT = input_value
                else:
                    print("Invalid timeout")
            except ValueError:
                print("Invalid timeout")

    elif MODE == "at-most-once":
        while Client_GLOBAL.TIMEOUT < 0:
            input_value = input("Please input timeout (seconds)(an integer greater than 0): ")
            try:
                input_value = int(input_value)
                if input_value > 0:
                    Client_GLOBAL.TIMEOUT = input_value
                else:
                    print("Invalid timeout")
            except ValueError:
                print("Invalid timeout")
            Client_GLOBAL.REQUEST_ID = 0
    
    elif MODE == "none":
        continue

    else:
        print("Invalid mode")

while Client_GLOBAL.FRESHNESS_INTERVAL < 0:
    input_value = input("Please input freshness interval (seconds)(an integer greater than 0): ")
    try:
        Client_GLOBAL.FRESHNESS_INTERVAL = int(input_value)
    except ValueError:
        print("Invalid freshness interval")

while True:
    choose = input("Test message loss? (y/n): ")
    if choose == "y":
        Client_GLOBAL.TEST_LOSS = True
        while Client_GLOBAL.POSSIBILITY_OF_LOSS == 0:
            input_value= input("Please input the possibility of message loss (1-100): ")
            try: # check integer
                input_value = int(input_value)
                if input_value >= 0 and input_value <= 100: # check greater than 0
                    Client_GLOBAL.POSSIBILITY_OF_LOSS = input_value
                else:
                    print("Invalid possiblity of loss")
            except ValueError:
                print("Invalid possiblity of loss")
        break
    elif choose == "n":
        # TEST_LOSS = False
        break
    else:
        print("Invalid input")

# build connection with client
# -------------need to implement----------------

if Client_GLOBAL.TIMEOUT > 0:
    Client_GLOBAL.CLIENT_SOCKET.settimeout(Client_GLOBAL.TIMEOUT)

SERVER_ADDRESS = ('localhost', 12345) # something like this

# -------------------------------------------------INITIALIZE the CLIENT: END------------------------------------------
#######################################################################################################################
# ---------------------------------------------RECEIVE and SEND the REQUEST: START-------------------------------------

while True:
    # get operation and parameters from user
    # -------------need to implement----------------
    print(">"*50 + "New Request" + "<"*50)
    print("Please input operation:\n \
          list files: list all shared files on the server\n \
          read: read shared files\n \
          write insert: insert new content into exit files\n \
          write append: write new content append to the exit files\n \
          register monitor: register monitor on specific files to receive updates\n \
          get file attribute: get attributes of shared files\n \
          exit: terminate the client")
    operation = input("Please input operation: ") # something like this
    
    # send request to server
    if operation == "list files":
        print("#"*50 + "Response from the Server" + "#"*50)

        Client_Get_file_list.get_file_list()
    # Read option: "read"
    # Read request: {"operation":"read", "pathname":pathname(str), "offset":offset(int), "length":length(int)}
    elif operation == "read":
        pathname = input("Please input pathname: ")
        offset = int(input("Please input offset: "))
        length = int(input("Please input length of read: "))

        print("#"*50 + "Response from the Server" + "#"*50)
        Client_Read_file.read_file(pathname,offset,length)

    # Write insert option: "write insert"
    # Write insert request: {"operation":"write_insert", "pathname":pathname(str), "offset":offset(int), "data":data(str)}
    elif operation == "write insert":
        pathname = input("Please input pathname: ")
        offset = int(input("Please input offset: "))
        data = input("Please input data: ")

        print("#"*50 + "Response from the Server" + "#"*50)
        Client_Write_file.write_insert(pathname,offset,data)

    # Non-idempotent operation
    # Write append option: "write append"
    # Write append request: {"operation":"write_append", "pathname":pathname(str), "data":data(str)}
    elif operation == "write append":
        pathname = input("Please input pathname: ")
        data = input("Please input data: ")

        print("#"*50 + "Response from the Server" + "#"*50)
        Client_Write_file.write_append(pathname,data)

    # Register Monitor option: "register monitor"
    # Register Monitor request: {"operation":operation(str), "pathname":pathname(str), "interval":t(int)}
    elif operation == "register monitor":
        pathname = input("Please input pathname: ")
        interval = int(input("Please input interval: "))

        print("#"*50 + "Response from the Server" + "#"*50)
        isSuccess = Client_Register_Monitor.register_monitor(pathname,interval)
        if isSuccess:
            # wait for update notification from the server
            Client_Wait_notification.wait_for_notification()


    # Idempotent operation
    # Get file attribute option: "get file attribute"
    # Get file attribute request: {"operation":operation(str), "pathname":pathname(str)}
    elif operation == "get file attribute":
        pathname = input("Please input pathname: ")

        print("#"*50 + "Response from the Server" + "#"*50)
        # return format: (t_mserver(int), length(int)) (tuple)
        return_value = Client_Get_file_attr.get_file_attr(pathname)
        t_mserver = return_value[0]
        length = return_value[1]
        if length == -1:
            print("File %s does not exist on the server" % pathname)
        else:
            print("Last modifed time of %s on the server is %d" % (pathname, t_mserver))
            print("Length of %s is %d bytes" % (pathname, length))

    # terminate the client
    elif operation == "exit":
        break

    else:
        print("#"*50 + "Response from the Server" + "#"*50)
        print("Invalid operation")

Client_GLOBAL.CLIENT_SOCKET.close()
# receive response from server done in Client_Send_and_Receive.py and specific operation file
# ---------------------------------------------RECEIVE and SEND the REQUEST: END-------------------------------------