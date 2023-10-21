import os
# return [string,string,...]
def get_file_list():
    file_list = os.listdir('Shared file')
    return file_list