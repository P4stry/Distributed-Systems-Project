import socket
# for test
# set TIMEOUT = 1

# -------------------------------------------------GLOBAL STATE: START------------------------------------------------
# freeshness interval
# Need to set by user!!!!!!!
FRESHNESS_INTERVAL = -1

# {pathname:{offset:int, end:int, T_c:int, T_mclient:int, content:string}}
CACHE = {}

TIMEOUT = -1
REQUEST_ID = -1

TEST_LOSS = False
POSSIBILITY_OF_LOSS = 0

CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # something like this
CLIENT_ADDRESS = ('localhost', 12344) # something like this
CLIENT_SOCKET.bind(CLIENT_ADDRESS) # something like this

SERVER_ADDRESS = ('localhost', 12345)

# -------------------------------------------------GLOBAL STATE: END---------------------------------------------------
