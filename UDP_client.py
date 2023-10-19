import socket

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address and port to send data to
server_address = ('localhost', 12345)

# Data to send to the server
message = "Hello Server"

# Send data to the server
client_socket.sendto(message.encode("utf-8"), server_address)

# Receive a response from the server
response, server_address = client_socket.recvfrom(1024)
print("Received {} bytes from {}:{}".format(len(response), *server_address))
print("Respond from {}:{} : {}".format(*server_address, response.decode("utf-8")))

# Close the socket
client_socket.close()

