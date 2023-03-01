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

        data = client_socket.recv(1024).decode()
        date = datetime.datetime.now()

        f = open("log.txt", "a")
        f.write("{}:{}:{}:{}\n".format(date,
                client_address[0], client_address[1], str(data)))
        f.close()

        client_socket.close()
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
