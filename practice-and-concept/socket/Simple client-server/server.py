#first of all import the socket library
import socket

# next xreate a socket object
s = socket.socket()
print("Socket successfully created")

#reserve a port on your computer in our case it's 12345 but it can be anything
port = 12345
''' Next bind to the port 
 we have not typed any ip in the ip field 
instead we have inputted an empty string 
 this makes the server listen to requests 
 coming from other computers on the network 
'''
s.bind(('',port))
print("socket blinded to %s"%(port))
#put the socket into listening mode
s.listen(5)
print("Socket is listening ")
# a forever loop until we interrupt it or 
# an error occurs 
while True:
    #Establish connection with client
    c,addr = s.accept()
    print("Got connection from",addr)
    # send a thankyou message to client .encoding to send byte type
    c.send("Thank you for connecting ".encode())
    #close the connection with client
    c.close()

    #breaking once  connecting closed
