import Client_Send_and_Receive

def register_monitor(pathname, t):
    # reponse format: {"isSuccess":isSuccess(bool)}
    request = {"operation":"register_monitor", "pathname":pathname, "interval":t}
    response = Client_Send_and_Receive.send_and_receive(request)
    isSuccess = response["isSuccess"]
    if isSuccess:
        print("Register monitor on "+ pathname + " successfully, expiration time is " + str(t))
        return True
    else:
        print("Register monitor fail")
        return False