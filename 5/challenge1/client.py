from ftplib import FTP
f = FTP('localhost')


username = input(">> Enter username: ")
password = input(">> Enter password: ")
ip = input(">> Enter IP server: ")
f.login(username, password)


def list():
    print(">>", str(f.nlst()))


def download(filename):
    fd = open(filename, "wb")
    f.retrbinary("RETR " + filename, fd.write, 1024)
    fd.close()
    print(f">> {filename} successfully downloaded")


def upload(filename):
    with open(filename, "rb") as file:
        f.storbinary(f"STOR {filename}", file)
    print(f">> File {filename} uploaded successfully")


def create_directory(dir):
    ftpResponse = f.mkd(dir)
    print(f">> {ftpResponse} successfully created")


def get_current_directory():
    print(">>", f.pwd())


while True:
    try:
        command = input(">> ")

        if "LIST" in command:
            list()
        elif "UPLOAD " in command:
            upload(command.split(" ")[1])
        elif "DOWNLOAD " in command:
            download(command.split(" ")[1])
        elif "CREATE DIR " in command:
            create_directory(command.split(" ")[2])
        elif "PWD" in command:
            get_current_directory()
        else:
            print(">> Command not found")
    except KeyboardInterrupt:
        f.quit()
    except Exception as e:
        print(">> [ERROR]", e)
