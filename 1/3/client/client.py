import socket
import sys


ip = input("Enter IP: ")
port = input("Enter port: ")

server_address = (ip, int(port))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

filename = input("Enter filename: ")

f = open(filename, "r")
client_socket.send(filename.encode())

file_data = str(f.read())
client_socket.send(file_data.encode())

data = client_socket.recv(1024).decode()
print(data)

client_socket.close()
sys.exit(0)
