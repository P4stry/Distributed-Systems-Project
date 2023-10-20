import Server
import os
# Server.FILE_ATTR = {pathname(str):{"t_mserver":t(int), "length":length(int)}}

# pathname: file name
# t: last modified time
# length: length of file
def update_file_attr(pathname,t):
    Server.FILE_ATTR[pathname]["t_mserver"] = t
    Server.FILE_ATTR[pathname]["length"] = os.path.getsize(pathname)
def get_file_attr(pathname):
    return Server.FILE_ATTR[pathname]["t_mserver"], Server.FILE_ATTR[pathname]["length"]