import os
import Server
'''
Description: A service that allows a user to read the content of a file

Parameter: pathname, offset(in bytes), the number of bytes to read from the file

Return: the given number of bytes of the file content starting from the designated offset in the file (the offset of the first byte in the file is 0)

Error message should be returned if the file does not exist on the server or if the offset exceeds the file length
'''

# return data or error message
def read_file(pathname,offset,length):
    try:
        f = open(pathname,'r')
    except OSError:
        return Server.Error.FILE_OPEN_ERROR
    
    max_offset = os.path.getsize(pathname) - 1
    if offset > max_offset or offset < 0:
        return Server.Error.FILE_SEEK_ERROR
    f.seek(offset)

    data = f.read(length)
    f.close()
    return data

# print(read_file('test.txt',4,10))