from datetime import datetime
import Server
'''
Description: 
A service that allows a user to monitor updates made to the content of a specified file at the server 
for a designated time period called monitor interval. After registration, the Internet address and the port number 
of the client are recorded by the server. During the monitoring interval, every time an update is made by any client to 
the content of the file, the updated file content is sent by the server to the registered client(s) through callback.
After the expiration of the monitor interval, the client record is removed from the server which will no longer deliver 
the file content to the client
Parameter: pathname, the length of monitor interval
Return: the updated file content
'''

# return True if registration is successful
# pathname: string
# address: "ip:port"
def register(pathname, address, t):
    curr_dt = datetime.now()
    timestamp = int(round(curr_dt.timestamp()))
    expiration = t + timestamp
    if pathname in Server.MONITORING:
        Server.MONITORING[pathname][address] = expiration
    else:
        Server.MONITORING[pathname] = {address:expiration}
    return True

# return list of clients to be notified
def callback_clients(pathname):
    alive_clients = []
    expired_clients = []
    curr_dt = datetime.now()
    timestamp = int(round(curr_dt.timestamp()))
    if pathname in Server.MONITORING:
        for address, expiration in Server.MONITORING[pathname].items():
            if expiration < timestamp:
                expired_clients.append(address) # remove the expired record
            else:
                alive_clients.append(address) # record the client to be notified
    else:
        pass

    for address in expired_clients:
        del Server.MONITORING[pathname][address]
    
    return alive_clients

# print(MONITORING)
# print(callback_clients('test.txt'))
# print(MONITORING)