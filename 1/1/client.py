import socket
import sys

server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

try:
    while True:
        val = input("Enter your value: ")
        client_socket.send(val.encode())

        print("Data sent")

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)
