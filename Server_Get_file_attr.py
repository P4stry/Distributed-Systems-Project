import Server
# Server.FILE_ATTR = {pathname(str):t(int)}

# pathname: file name
# t: last modified time
def update_file_attr(pathname,t):
    Server.FILE_ATTR[pathname] = t
def get_file_attr(pathname):
    return Server.FILE_ATTR[pathname]