import Server_GLOBAL
import Server_Monitor
import Server_Get_file_attr
from datetime import datetime
import os
'''
Description: The service inserts the sequence of bytes into the file at the designated offset in the file. The original content of the file after the offset is pushed forward.

Parameter: pathname, offset (in bytes), a sequence of bytes to write into the file

Return: an acknowledgement on successful insertion

Error message should be returned if the file does not exist on the server or if the offset exceeds the file length
'''

# return an acknowledgement, clients to be notified, new content
def write_insert(pathname, offset, data):
    check_exist = os.path.isfile(pathname)
    if not check_exist:
        return Server_GLOBAL.Error.FILE_NOT_EXIST
    try:
        f = open(pathname, 'r')
    except OSError:
        return Server_GLOBAL.Error.FILE_OPEN_ERROR
    max_offset = os.path.getsize(pathname) - 1
    if offset > max_offset or offset < 0:
        return Server_GLOBAL.Error.FILE_SEEK_ERROR
    
    current_content = f.read()
    f.close()

    # write insert
    new_content = current_content[:offset] + data + current_content[offset:]
    f = open(pathname, 'w')
    f.write(new_content)
    f.close()

    # update file attribute
    curr_dt = datetime.now()
    timestamp = int(round(curr_dt.timestamp()))
    Server_Get_file_attr.update_file_attr(pathname, timestamp)

    # update clients to be notified
    clients = Server_Monitor.callback_clients(pathname)

    return True, clients, new_content
    # Server sends new content to the client requesting write operation anyway

def write_append(pathname, data):
    check_exist = os.path.isfile(pathname)
    if not check_exist:
        return Server_GLOBAL.Error.FILE_NOT_EXIST
    try:
        f = open(pathname, 'a')
    except OSError:
        return Server_GLOBAL.Error.FILE_OPEN_ERROR

    # write append
    f.write(data)
    f.close()

    # current content
    f = open(pathname, 'r')
    new_content = f.read()
    f.close()

    # update file attribute
    curr_dt = datetime.now()
    timestamp = int(round(curr_dt.timestamp()))
    Server_Get_file_attr.update_file_attr(pathname, timestamp)

    # update clients to be notified
    clients = Server_Monitor.callback_clients(pathname)

    return True, clients, new_content

# Test
# print(write_insert('test.txt', 1, 'b'))
# return_value = (True, ['192.168.0.1'], 'abcd')
# isSuccess = return_value[0]
# clients = return_value[1]
# content = return_value[2]
# print(isSuccess)
# print(clients)
# print(content)