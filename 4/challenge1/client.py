import socket
import sys
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address, port))


def send_msg(sock):
    try:
        while True:
            data = input("> ")
            sock.send(data.encode())

            print(f"Sent: {data}")
    except KeyboardInterrupt or EOFError:
        server.close()
    print("Client disconnected")
    sys.exit(0)


def recv_msg(sock):
    try:
        while True:
            data = sock.recv(2048).decode()
            print(f'Received: {data}', end="\n> ")
    except KeyboardInterrupt:
        server.close()
    print("Client disconnected")
    sys.exit(0)


def main():
    Thread(target=send_msg, args=(server,)).start()
    Thread(target=recv_msg, args=(server,)).start()


if __name__ == "__main__":
    main()
