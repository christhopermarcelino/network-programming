import socket
import select
import sys
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address, port))
id = None


def send_msg(sock):
    print("> ", end="")
    try:
        while True:
            data = input()

            target_id = None

            if data == "list":
                data = f"list {id}"
                target_id = "Server"
            else:
                target_id = data.split(" ", 2)[1]

            sock.send(data.encode())

            print(f"Sent to: {target_id}")
    except KeyboardInterrupt or EOFError:
        server.close()
    print("Client disconnected")
    sys.exit(0)


def recv_msg(sock):
    try:
        while True:
            data = sock.recv(2048).decode()
            sender, message = data.split(" ", 1)
            print(f'From {sender}: {message}', end="\n> ")
    except KeyboardInterrupt:
        server.close()
    print("Client disconnected")
    sys.exit(0)


def main():
    id = server.recv(36).decode()
    print(f"Connected to server with id: {id}")
    Thread(target=send_msg, args=(server,)).start()
    Thread(target=recv_msg, args=(server,)).start()


if __name__ == "__main__":
    main()
