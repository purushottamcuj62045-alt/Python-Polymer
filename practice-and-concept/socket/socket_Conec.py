#How to use socket interface of python to connect a server using client tcp socket 
import socket
import sys

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("Socket failed to create")
    sys.exit()

print("Socket created")

target_host = input("Enter a target hostname to connect: ")
target_port = int(input("Enter the target port: "))

try:
    sock.connect((target_host, target_port))
    print("Socket connected")
    print("Target host:", target_host)
    print("Target port:", target_port)
    sock.shutdown(2)

except socket.error as err:
    print("Failed to connect")
    print("Reason:", str(err))
    sys.exit()
