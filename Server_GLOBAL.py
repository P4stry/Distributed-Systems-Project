from enum import Enum
import socket

# for test
# set TIMEOUT = 1

# -------------------------------------------------GLOBAL STATE: START------------------------------------------------

class Error(Enum):
    FILE_NOT_EXIST = 0
    FILE_OPEN_ERROR = 1
    FILE_SEEK_ERROR = 2

# {pathname(str):t(int)}
FILE_ATTR = {}

# {pathname(str):{address(str):expiration(int)(sec)}}
# MONITORING = {"test.txt":{"192.168.0.1":1797625518, "192.168.0.2":1597625518}}
MONITORING = {}

# log requests and replies history
# {address(str):{requestId(int):reply(str)}}
HISTORY = {}

# for at-most-once and at-least-once and message loss test
# Need to set by user!!!!!!!
SLEEP_INTERVAL = -1
TEST_LOSS = False
POSSIBILITY_OF_LOSS = 0

# build connection with client
# -------------need to implement----------------
# something like this
SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SERVER_ADDRESS = ('localhost', 12345)
SERVER_SOCKET.bind(SERVER_ADDRESS)

# -------------------------------------------------GLOBAL STATE: END---------------------------------------------------
