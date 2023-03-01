import socket
import sys

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ')

try:
    while True:
        file_data = str(input())

        with open(file_data, "r") as fd:
            data = fd.read()
            client_socket.send(data.encode())

        data = client_socket.recv(1024).decode()

        print(data)
        print(">> ")
except KeyboardInterrupt:
    print('Client shutting down...')
    client_socket.close()
    sys.exit(0)
