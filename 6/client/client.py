import socket
import os

BUFFER_SIZE = 3

ip = input("Enter IP: ")
port = int(input("Enter port: "))
file_name = input("Enter filepath: ")

server_address = (ip, port)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# get filesize
# file_size = os.path.getsize(file_name)
file_size = os.stat(file_name).st_size


#  send filename and filesize to server
message = f"{file_name} {file_size}"
client_socket.sendto(message.encode(), server_address)

# open file and send file data to server
with open(file_name, "r") as fp:
    while data := fp.read(BUFFER_SIZE):
        client_socket.sendto(data.encode(), server_address)

client_socket.sendto(b'', server_address)

data, server_address = client_socket.recvfrom(1024)
print(f"Server {server_address} says: {data.decode()}")

client_socket.close()
