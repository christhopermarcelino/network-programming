import socket
import sys


ip = input("Enter IP: ")
port = input("Enter port: ")

server_address = (ip, int(port))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

val = input("Enter data: ")
client_socket.send(val.encode())

data = client_socket.recv(1024).decode()
print(data)

client_socket.close()
sys.exit(0)
