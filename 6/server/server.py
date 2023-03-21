import socket
import os

BUFFER_SIZE = 1024

server_address = ("192.168.43.72", 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
is_connect = False


def get_file_percentage(fp, file_size):
    fp.seek(0, 2)
    actual_file_size = fp.tell()

    return actual_file_size / int(file_size) * 100


while True:
    server_socket.settimeout(None)
    data, client_address = server_socket.recvfrom(1024)
    is_connect = True
    server_socket.settimeout(1)

    if not is_connect:
        continue

    file_name, file_size = data.decode().split(" ")
    print(f"Received {file_name} with size {file_size}")
    fp = open(file_name, "w+")

    while True:
        try:
            server_socket.settimeout(1)
            data_file, client_address = server_socket.recvfrom(BUFFER_SIZE)

            fp.write(data_file.decode())
        except socket.timeout:
            break

    percentage = get_file_percentage(fp, file_size)
    message = f"File {file_name} downloaded {percentage}%"
    print(message)
    server_socket.sendto(message.encode(), client_address)
    fp.close()
    is_connect = False
