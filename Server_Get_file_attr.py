import Server_GLOBAL
import os
# Server.FILE_ATTR = {pathname(str):{"t_mserver":t(int), "length":length(int)}}

# pathname: file name
# t: last modified time
# length: length of file
def update_file_attr(pathname,t):
    if pathname not in Server_GLOBAL.FILE_ATTR:
        Server_GLOBAL.FILE_ATTR[pathname] = {}
    Server_GLOBAL.FILE_ATTR[pathname]["t_mserver"] = t
    Server_GLOBAL.FILE_ATTR[pathname]["length"] = os.path.getsize(pathname)
def get_file_attr(pathname):
    check = os.path.isfile(pathname)
    # file not exist
    if not check:
        return -1, -1
    # file exist but not in FILE_ATTR
    if pathname not in Server_GLOBAL.FILE_ATTR:
        Server_GLOBAL.FILE_ATTR[pathname] = {}
        Server_GLOBAL.FILE_ATTR[pathname]["t_mserver"] = -1 # do not know the last modified time
        Server_GLOBAL.FILE_ATTR[pathname]["length"] = os.path.getsize(pathname)
    return Server_GLOBAL.FILE_ATTR[pathname]["t_mserver"], Server_GLOBAL.FILE_ATTR[pathname]["length"]