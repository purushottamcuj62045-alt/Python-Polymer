#How web servers work internally
import socket

s = socket.socket()
s.bind(('localhost', 8080))
s.listen(1)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    response = b"HTTP/1.1 200 OK\n\nHello World"
    conn.send(response)
    conn.close()
