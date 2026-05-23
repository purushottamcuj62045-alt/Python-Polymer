import socket
import sys
import os
import struct

TCP_IP = "127.0.0.1"
TCP_PORT = 1456
BUFFER_SIZE = 65536

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conn():
    print("Sending server request.........")
    try:
        s.connect((TCP_IP, TCP_PORT))
        print("Connection Successful.")
    except Exception as e:
        print("Connection unsuccessful")
        print(e)

def upld(file_name):
    print("\nUploading file: {}...".format(file_name))

    try:
        content = open(file_name, "rb")
    except Exception as e:
        print("Couldn't open file.")
        print(e)
        return

    try:
        s.send(b"UPLD")
    except Exception as e:
        print("Couldn't make server request.")
        print(e)
        return

    try:
        s.recv(BUFFER_SIZE)
        s.sendall(struct.pack("h", len(file_name)))
        s.sendall(file_name.encode())
        s.recv(BUFFER_SIZE)
        s.sendall(struct.pack("i", os.path.getsize(file_name)))
    except Exception as e:
        print("Error sending file details")
        print(e)
        return

    try:
        l = content.read(BUFFER_SIZE)
        print("\nSending...")

        while l:
            s.sendall(l)
            l = content.read(BUFFER_SIZE)

        content.close()

        upload_time = struct.unpack("f", s.recv(4))[0]
        upload_size = struct.unpack("i", s.recv(4))[0]

        print("\nSent file: {}\nTime elapsed: {}s\nFile size: {}b".format(
            file_name, upload_time, upload_size
        ))

    except Exception as e:
        print("Error sending file")
        print(e)

def list_files():
    print("Requesting files")

    try:
        s.sendall(b"LIST")
    except Exception as e:
        print("Couldn't make server request.")
        print(e)
        return

    try:
        number_of_files = struct.unpack("i", s.recv(4))[0]

        for i in range(number_of_files):
            file_name_size = struct.unpack("i", s.recv(4))[0]
            file_name = s.recv(file_name_size).decode()
            file_size = struct.unpack("i", s.recv(4))[0]

            print("\t{} - {}b".format(file_name, file_size))

            s.sendall(b"1")

        total_directory_size = struct.unpack("i", s.recv(4))[0]

        print("Total directory size: {}b".format(total_directory_size))

    except Exception as e:
        print("Couldn't retrieve listing")
        print(e)
        return

    try:
        s.sendall(b"1")
    except Exception as e:
        print("Couldn't get final server confirmation")
        print(e)

def dwld(file_name):
    print("Downloading file: {}".format(file_name))

    try:
        s.sendall(b"DWLD")
    except Exception as e:
        print("Couldn't make server request.")
        print(e)
        return

    try:
        s.recv(BUFFER_SIZE)

        s.sendall(struct.pack("h", len(file_name)))
        s.sendall(file_name.encode())

        file_size = struct.unpack("i", s.recv(4))[0]

        if file_size == -1:
            print("File does not exist.")
            return

    except Exception as e:
        print("Error checking file")
        print(e)
        return

    try:
        s.sendall(b"1")

        output_file = open(file_name, "wb")

        bytes_received = 0

        print("\nDownloading...")

        while bytes_received < file_size:
            l = s.recv(BUFFER_SIZE)

            output_file.write(l)

            bytes_received += len(l)

        output_file.close()

        print("Successfully downloaded {}".format(file_name))

        s.sendall(b"1")

        time_elapsed = struct.unpack("f", s.recv(4))[0]

        print("Time elapsed: {}s\nFile size: {}b".format(
            time_elapsed, file_size
        ))

    except Exception as e:
        print("Error handling download")
        print(e)

def delf(file_name):
    print("Deleting File: {}....".format(file_name))

    try:
        s.send(b"DELF")
        s.recv(BUFFER_SIZE)

    except Exception as e:
        print("Couldn't connect to server.")
        print(e)
        return

    try:
        s.send(struct.pack("h", len(file_name)))
        s.send(file_name.encode())

        file_exists = struct.unpack("i", s.recv(4))[0]

        if file_exists == -1:
            print("The file does not exist on server")
            return

    except Exception as e:
        print("Couldn't determine file existence")
        print(e)
        return

    try:
        confirm_delete = input(
            "Are you sure you want to delete {}? (Y/N)\n".format(file_name)
        ).upper()

        while confirm_delete not in ["Y", "N", "YES", "NO"]:
            confirm_delete = input("Please enter Y or N: ").upper()

    except Exception as e:
        print("Error:", e)
        return

    try:
        if confirm_delete in ["Y", "YES"]:
            s.send(b"Y")

            delete_status = struct.unpack("i", s.recv(4))[0]

            if delete_status == 1:
                print("File successfully deleted")
            else:
                print("File failed to delete")

        else:
            s.send(b"N")
            print("Delete abandoned by user!")

    except Exception as e:
        print("Couldn't delete file")
        print(e)

def quit_client():
    try:
        s.sendall(b"QUIT")
        s.recv(BUFFER_SIZE)
        s.close()

        print("Server connection closed")

    except Exception as e:
        print(e)

print("""
Welcome to the FTP client.

Call one of the following functions:

CONN           : Connect to server
UPLD file_path : Upload file
LIST           : List files
DWLD file_path : Download file
DELF file_path : Delete file
QUIT           : Exit
""")

while True:
    prompt = input("\nEnter a command: ")

    if prompt[:4].upper() == "CONN":
        conn()

    elif prompt[:4].upper() == "UPLD":
        upld(prompt[5:])

    elif prompt[:4].upper() == "LIST":
        list_files()

    elif prompt[:4].upper() == "DWLD":
        dwld(prompt[5:])

    elif prompt[:4].upper() == "DELF":
        delf(prompt[5:])

    elif prompt[:4].upper() == "QUIT":
        quit_client()
        break

    else:
        print("Command not recognised; please try again")
