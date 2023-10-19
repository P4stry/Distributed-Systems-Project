import Client
import Server_Monitor

def register_monitor(pathname, t):
    # marshalling
    # send operation and parameters to server
    # receive response from server
    # unmarshalling

    # reponse format: {"isSuccess":isSuccess(bool)}
    isSuccess = Server_Monitor.register(pathname,t) # for test
    return isSuccess
    # if isSuccess:
    #     print("Register monitor on "+ pathname + " successfully, expiration time is " + str(t))
    #     return True
    # else:
    #     print("Register monitor fail")
        