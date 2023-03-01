import select
import socket
import sys
from threading import Thread

clients = []


class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []
        self.client_counter = 0

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

    def run(self):
        self.open_socket()
        input = [self.server]
        running = 1
        while running:
            inputready, outputready, exceptready = select.select(input, [], [])

            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    client_socket, client_address = self.server.accept()

                    self.client_counter += 1
                    client_name = f"Client {self.client_counter}"

                    c = Client(client_socket, client_address, client_name)
                    c.start()

                    clients.append((client_socket, client_address))

                    self.threads.append(c)
                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

         # close all threads
        self.server.close()
        for c in self.threads:
            c.join()


class Client(Thread):
    def __init__(self, client, address, name):
        Thread.__init__(self)
        self.client = client
        self.address = address
        self.name = name
        self.size = 1024

    def receive(self):
        return self.client.recv(self.size).decode()

    def send(self, s, data):
        s.send(data.encode())

    def run(self):
        running = 1

        try:
            while running:
                request = self.receive()

                filename, filedata = request.split('|')

                with open("buffer.txt", "w+") as fd:
                    fd.write(filedata)

                data = "|".join([filename, filedata, self.name])

                broadcast_clients = clients.copy()
                broadcast_clients.remove((self.client, self.address))

                for bc in broadcast_clients:
                    send_thread = Thread(target=self.send, args=(bc[0], data))
                    send_thread.start()

        except KeyboardInterrupt:
            self.client.close()
            running = 0


if __name__ == "__main__":
    s = Server()
    s.run()
