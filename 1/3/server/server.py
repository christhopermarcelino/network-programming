import socket
import sys
import datetime


server_address = ('localhost', 5000)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

try:
    while True:
        client_socket, client_address = server_socket.accept()

        filename = client_socket.recv(20).decode()
        data = client_socket.recv(1024).decode()

        print("Filename", filename)
        f = open(filename, "a")
        f.write(data)
        f.close()

        client_socket.close()
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
