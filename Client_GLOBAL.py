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

CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
CLIENT_ADDRESS = ('172.20.10.2', 12344)
CLIENT_SOCKET.bind(CLIENT_ADDRESS)

SERVER_ADDRESS = ('172.20.10.3', 9999)

# -------------------------------------------------GLOBAL STATE: END---------------------------------------------------
