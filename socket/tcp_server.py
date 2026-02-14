#Creating a tcp server which sends data to a client and also recieve data to a client
import socket

server_socket =socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.bind(('127.0.0.1',12345))
server_socket.listen(5)

while True:
    print("Server waiting for connection")
    client_socket,addr=server_socket.accept()
    while True:
        data=client_socket.recv(1024)
        if not data or data.decode('utf-8')=='END':
            break
        print("Recived from client client: %s",data.decode('utf-8'))
        try:
            client_socket.send(bytes('Hey client','utf-8'))
        except:
            print("Exited by user")
            
    client_socket.close()

server_socket.close()
