import socket
import sys
from threading import Thread

MESSAGE_SIZE = 2048
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address, port))

id = None
is_joined = False
group_id = None


def receive():
    return server.recv(MESSAGE_SIZE).decode()


def send(data):
    server.send(data.encode())


def receive_thread():
    try:
        while True:
            data = receive()

            keyword, message = data.split(" ", 1)

            if keyword == "ID":
                get_unique_id(message)
            elif keyword == "LIST":
                get_group_list(message)
            elif keyword == "CREATE" or keyword == "JOIN":
                new_group(message)
            elif keyword == "EXIT":
                exit()
            else:  # CHAT
                get_chat(message)

    except KeyboardInterrupt:
        print('Client shutting down...')
        server.close()


def get_group_list(message):
    print("List of groups:")
    print(message)


def new_group(g_id):
    global group_id, is_joined
    group_id = g_id
    is_joined = True

    print(f"Welcome to group {group_id}")


def get_chat(data):
    sender_id, message = data.split(" ", 1)
    print(f"From {sender_id}: {message}", end="\n> ")


def print_welcome_message():
    print("Type your option:")
    print("<> LIST (view group list) ")
    print("<> CREATE id (create new group)")
    print("<> JOIN id (join existing group)")
    print("<> EXIT (dsconnect from server)")


def exit():
    global is_joined, id, group_id

    is_joined = False
    id = None
    group_id = None
    print("You have left the group")
    disconnect()


def disconnect():
    print('Client shutting down...')
    server.close()
    sys.exit(0)


def send_thread():
    global id

    try:
        while True:
            data = None

            try:
                data = input("> ")
            except EOFError:
                disconnect()

            keyword = None

            if data == "":
                print("Please type something!", end="\n> ")
                continue
            elif data == "EXIT":
                send(f"EXIT {id} {group_id}")
                disconnect()
            elif data == "LIST":
                keyword = "LIST"
            else:
                keyword = data.split(" ", 1)[0]

            if is_joined and keyword in ["LIST", "CREATE", "JOIN"]:
                print("Keyword not allowed. Please send a message instead!", end="\n> ")
                continue
            elif not is_joined and keyword not in ["LIST", "CREATE", "JOIN"]:
                print("Message failed. Please join or create a group first!", end="\n> ")
                continue

            if keyword == "LIST":
                data = f"LIST {id}"
            elif keyword == "CREATE" or keyword == "JOIN":
                data = f"{data} {id}"
            else:
                data = f"CHAT {id} {data}"

            send(data)
    except KeyboardInterrupt:
        print('Client shutting down...')
        server.close()


def get_unique_id(unique_id):
    global id

    id = unique_id

    print(f"You are assigned as {unique_id}", end="\n> ")


def main():
    print_welcome_message()
    Thread(target=send_thread).start()
    Thread(target=receive_thread).start()


if __name__ == "__main__":
    main()
