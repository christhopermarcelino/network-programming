import socket
import sys
from threading import Thread
from uuid import uuid4

MESSAGE_SIZE = 2048
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address, port))
server.listen(100)
list_of_clients_to_group = {}  # client_id = group_id
list_of_groups = {}  # group_id = [client_id, ...]


def client_thread(conn):
    while True:
        try:
            message = receive(conn)

            keyword = message.split(" ", 1)[0]

            # LIST, CREATE, JOIN, SEND MESSAGE
            if keyword == "EXIT":
                _, client_id, group_id = message.split(" ", 2)
                remove(conn, client_id, group_id)
            elif keyword == "LIST":
                send_group_list(conn)
            elif keyword == "CREATE":
                _, group_id, client_id = message.split(" ", 2)
                create_group(conn, group_id, client_id)  # CREATE id
            elif keyword == "JOIN":
                _, group_id, client_id = message.split(" ", 2)
                join_group(conn, group_id, client_id)
            else:  # CHAT
                _, client_id, message = message.split(" ", 2)
                send_message_to_group(client_id, message)
        except KeyboardInterrupt:
            server.close()
            print("Server closed")
            sys.exit(0)


def send_message_to_group(client_id, message):
    client_group_id = list_of_clients_to_group[client_id]  # group_id
    # [(client_id, conn), ...]
    list_of_clients = list_of_groups[client_group_id]

    for client in list_of_clients:
        id, conn = client
        if id != client_id:
            message_to_send = f"CHAT {client_id} {message}"
            send(conn, message_to_send)


def create_group(conn, group_id, client_id):
    list_of_clients_to_group[client_id] = group_id

    sock = (client_id, conn)
    if group_id in list_of_groups:
        list_of_groups[group_id].append(sock)
    else:
        list_of_groups[group_id] = [sock]

    message = f"CREATE {group_id}"
    send(conn, message)


def join_group(conn, group_id, client_id):
    list_of_clients_to_group[client_id] = group_id

    if group_id in list_of_groups:
        list_of_groups[group_id].append((client_id, conn))
    else:
        list_of_groups[group_id] = [(client_id, conn)]

    message = f"JOIN {group_id}"
    send(conn, message)


def get_group_list():
    global list_of_groups

    return str(list(list_of_groups.keys()))[1:-1].replace(", ", "\n").replace("'", "")


def send_group_list(conn):
    group_list = get_group_list()
    message = f"LIST {group_list}"
    send(conn, message)


def remove(conn, client_id, group_id):
    list_of_groups[group_id].remove((client_id, conn))
    del list_of_clients_to_group[client_id]
    send(conn, "EXIT ")
    print(client_id + " disconnected")
    conn.close()


def send(conn, message):
    conn.send(message.encode())


def receive(conn):
    return conn.recv(MESSAGE_SIZE).decode()


def assign_unique_id(conn):
    unique_id = str(uuid4())
    client_list = list(list_of_clients_to_group.keys())
    while unique_id in client_list:
        unique_id = str(uuid4())

    list_of_clients_to_group[unique_id] = None

    print(addr[0] + " connected")
    message = f"ID {unique_id}"
    send(conn, message)


while True:
    conn, addr = server.accept()

    assign_unique_id(conn)

    Thread(target=client_thread, args=(conn,)).start()
