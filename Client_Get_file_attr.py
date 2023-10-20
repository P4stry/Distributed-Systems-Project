import Client_Send_and_Receive

def get_file_attr(pathname):
    # reponse format: {"T_mserver":t_mserver(int), "length":length(int)}
    # t_mserver: last modified time on the server
    # length: length of file
    request = {"operation":"get_file_attr", "pathname":pathname}
    response = Client_Send_and_Receive.send_and_receive(request)
    return response["T_mserver"], response["length"]