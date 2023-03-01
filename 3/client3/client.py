from threading import Thread
import socket
import sys

MESSAGE_SIZE = 1024
server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)


def receive():
    return client_socket.recv(MESSAGE_SIZE).decode()


def send(data):
    client_socket.send(data.encode())


def receiveThread():
    try:
        while True:
            # filename, data, sender
            payload = receive()

            filename, data, sender = payload.split('|')

            with open(filename, "w+") as fr:
                fr.write(data)

            print(
                f"Menerima file dari {sender}. Nama file: {filename}", end="\n>> ")
    except KeyboardInterrupt:
        print('Client shutting down...')
        client_socket.close()


def sendThread():
    try:
        while True:
            filename = str(input())

            fd = None

            try:
                fd = open(filename, "r")
            except IOError:
                print(f"Could not read file: {filename}")
                continue

            filedata = fd.read()
            fd.close()

            request = "|".join([filename, filedata])

            send(request)

            print(">> ")
    except KeyboardInterrupt:
        print('Client shutting down...')
        client_socket.close()


def main():
    try:
        print(">> ")

        receive_thread = Thread(target=receiveThread)
        send_thread = Thread(target=sendThread)

        receive_thread.start()
        send_thread.start()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
    sys.exit(0)
