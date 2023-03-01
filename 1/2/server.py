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

        if data == 'asklog':
            f = open("log.txt", "r")

            client_socket.send(f.read().encode())

            f.close()
        else:
            date = datetime.datetime.now()

            format_string = "{}:{}:{}:{}".format(date,
                                                 client_address[0], client_address[1], str(data))

            f = open("log.txt", "a")
            f.write(format_string + "\n")
            f.close()

            client_socket.send("({})".format(format_string).encode())

        client_socket.close()
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
