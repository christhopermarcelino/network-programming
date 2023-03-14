import socket
import sys
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address, port))
server.listen(100)
list_of_clients = []


def clientthread(conn, addr):
    while True:
        try:
            message = conn.recv(2048).decode()
            if message:
                result = str(eval(message))
                message_to_send = f"{message} = {result}"
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except ConnectionResetError:
            remove(conn)
        except KeyboardInterrupt:
            server.close()
            print("Server closed")
            sys.exit(0)
        except Exception as e:
            message_to_send = f"[ERROR] {e}"
            broadcast(message_to_send, conn)


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
        print(str(connection) + " disconnected")


while True:
    try:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        print(addr[0] + " connected")
        Thread(target=clientthread, args=(conn, addr)).start()
    except KeyboardInterrupt:
        server.close()
        print("Server closed")
        break
