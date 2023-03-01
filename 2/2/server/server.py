import select
import sys
import socket


def is_palindrome(s):
    return "yes" if s == s[::-1] else "no"


server_address = ('localhost', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]


try:
    while True:
        read_ready, write_ready, error = select.select(input_socket, [], [])
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
            else:
                data_received = sock.recv(1024).decode()

                datas = data_received.split()

                result = ""

                for data in datas:
                    result += str(data) + " - " + \
                        str(is_palindrome(data)) + '\n'

                with open("result.txt", "w+") as fr:
                    fr.write(result)

                sock.send(result.encode())

                sock.close()
                input_socket.remove(sock)
except KeyboardInterrupt:
    print('Server shutting down...')
    server_socket.close()
    sys.exit(0)
