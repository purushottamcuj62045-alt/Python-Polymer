import socket
import sys
import time
import os
import struct
print("\nwelcome to FTP server.\n\nTo get started, connect a client.")
TCP_IP = "127.0.0.1"
TCP_PORT = 1456
BUFFER_SIZE =65536
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()
print("\nconnected to address: {}".format(addr))
def upld():
    conn.sendall(b"1")
    file_name_size = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_size).decode()
    conn.sendall(b"1")
    file_size = struct.unpack("i", conn.recv(4))[0]
    start_time = time.time()
    output_file = open(file_name, "wb")
    bytes_received = 0
    print("\nReceiving...")
    while bytes_received < file_size:
        l = conn.recv(BUFFER_SIZE)
        if not l:
            break
        output_file.write(l)
        bytes_received += len(l)
    output_file.close()
    print("\nReceived file: {}".format(file_name))
    conn.sendall(struct.pack("f", time.time() - start_time))
    conn.sendall(struct.pack("i", file_size))
def list_files():
    print("Listening Files.....")
    listing = os.listdir(os.getcwd())
    conn.sendall(struct.pack("i",len(listing)))
    total_directory_size =0
    for  i in listing:
        conn.sendall(struct.pack("i",len(i)))
        conn.sendall(i.encode())
        file_size = os.path.getsize(i)
        conn.sendall(struct.pack("i",file_size))
        total_directory_size += file_size
        conn.recv(BUFFER_SIZE)
    conn.sendall(struct.pack("i",total_directory_size))
    conn.recv(BUFFER_SIZE)
    print("Successfully Sent file listing")
def dwld():
    conn.sendall(b"1")
    file_name_length = struct.unpack("h",conn.recv(2))[0]
    file_name = conn.recv(file_name_length).decode()
    print(file_name)
    if os.path.isfile(file_name):
        conn.sendall(struct.pack("i",os.path.getsize(file_name)))
    else:
        print("FIle name is not valid")
        conn.sendall(struct.pack("i",-1))
        return
    conn.recv(BUFFER_SIZE)
    start_time = time.time()
    print("Sending file........")
    content= open(file_name,"rb")
    l= content.read(BUFFER_SIZE)
    while l:
        conn.sendall(1)
        l= content.read(BUFFER_SIZE)
    content.close()
    conn.recv(BUFFER_SIZE)
    conn.sendall(struct.pack("f",time.time()-start_time))
def delf():
    conn.sendall(b"1")
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length).decode()
    if os.path.isfile(file_name):
        conn.sendall(struct.pack("i", 1))
    else:
        conn.sendall(struct.pack("i", -1))
        return
    confirm_delete = conn.recv(BUFFER_SIZE).decode()
    if confirm_delete == "Y":
        try:
            os.remove(file_name)
            print("File deleted successfully")
            conn.sendall(struct.pack("i", 1))
        except:
            print("Failed to delete {}".format(file_name))
            conn.sendall(struct.pack("i", -1))
    else:
        print("Delete abandoned by client!")
def quit_server():
    conn.sendall(b"1")
    conn.close()
    s.close()
    os.execl(sys.executable, sys.executable, *sys.argv)
while True:
    print("\n\nWaiting for instruction")
    data = conn.recv(BUFFER_SIZE).decode()
    print("\nReceived instruction: {}".format(data))
    if data == "UPLD":
        upld()
    elif data == "LIST":
        list_files()
    elif data == "DWLD":
        dwld()
    elif data == "DELF":
        delf()
    elif data == "QUIT":
        quit_server()
    data = None
