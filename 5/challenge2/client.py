from ftplib import FTP
from zipfile import ZipFile
import os


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


def upload_zip_file(path):
    _, filename = path.split("\\", 1)
    f.storbinary(f"STOR {filename}", open(path, "rb"))


def change_directory(dir):
    f.cwd(dir)


def remove_dir(dir):
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    os.rmdir(dir)


def upload_and_extract(path):
    foldername = path.split(".")[0]
    with ZipFile(path, 'r') as zObject:
        zObject.extractall(path=foldername)

    create_directory(foldername)

    change_directory(foldername)

    for file in os.listdir(foldername):
        full_path = os.path.join(foldername, file)
        if os.path.isfile(full_path):
            upload_zip_file(full_path)

    change_directory("/")
    remove_dir(foldername)
    print(f">> File {foldername} extracted and uploaded successfully")


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
        elif "UPTRACT " in command:
            upload_and_extract(command.split(" ")[1])
        else:
            print(">> Command not found")
    except KeyboardInterrupt:
        f.quit()
    except Exception as e:
        print(">> [ERROR]", e)
