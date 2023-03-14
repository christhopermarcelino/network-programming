import socket
import sys
from threading import Thread
from uuid import uuid4


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address, port))
server.listen(100)
list_of_clients = {}


def clientthread(conn, addr):
    while True:
        try:
            message = conn.recv(2048).decode()

            keyword = message.split(" ", 1)[0]

            if keyword == "list":
                # list sender_id
                all_clients = str(list(list_of_clients.keys()))[
                    1:-1].replace(", ", "\n").replace("'", "")

                message_to_send = f"Server \n{all_clients}"

                send(conn, None, message_to_send)
            elif keyword == "private":
                # private target_id message
                _, target_id, message = message.split(" ", 2)
                message_to_send = f"{target_id} {message}"
                send(conn, target_id, message_to_send)
            else:
                conn.close()
        except KeyboardInterrupt:
            server.close()
            print("Server closed")
            sys.exit(0)


def send(conn, target_id, message):
    if target_id is None:
        conn.send(message.encode())
        return

    if target_id not in list_of_clients:
        message = "Server Client not found!"
        conn.send(message.encode())
        return

    list_of_clients[target_id].send(message.encode())


def broadcast(message, connection):
    print("Broadcasting message: " + message)
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
        print(connection + " disconnected")


while True:
    conn, addr = server.accept()

    unique_id = str(uuid4())
    while unique_id in list_of_clients:
        unique_id = str(uuid4())

    list_of_clients[unique_id] = conn

    print(addr[0] + " connected")
    conn.send(unique_id.encode())
    Thread(target=clientthread, args=(conn, addr)).start()
