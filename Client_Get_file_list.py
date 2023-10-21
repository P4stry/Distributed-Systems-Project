import Client_Send_and_Receive
def get_file_list():
    request = {"operation":"list_files"}
    # response format: {"file_list":file_list(list)}
    response = Client_Send_and_Receive.send_and_receive(request)
    file_list = response["file_list"]
    if file_list:
        for file_name in file_list:
            print(file_name)
    else:
        print("No file in the server")