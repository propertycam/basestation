'''
Basestation recieves photos captured by propertycam camera units.
'''

import socket
import os


# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the socket to a port
#server_address = ('localhost', 50000)
server_address = ('', 50000)
sock.bind(server_address)
sock.listen()
print('Propertycam basestation listening on %s port %s' % server_address)

# Initialize snapshot number
snapnum = 0

# Create directory to store snaps
snapdir = 'snaps'
if not os.path.exists(snapdir):
    os.mkdir(snapdir)

# Continuously accept and handle connections
while True:

    # Wait for connection
    connection, client_addr = sock.accept()
    print('Connection from ', client_addr)

    # Create file to write snapshot to
    snapnum = snapnum + 1
    file = open(snapdir + '/' + str(snapnum).zfill(5) + '.jpg', 'wb')

    # Receive parts
    buffer_size = 1024
    buffer = connection.recv(buffer_size)
    partnum = 1
    while(buffer):
        print('Recieved part ', partnum)
        file.write(buffer)
        buffer = connection.recv(buffer_size)
        partnum = partnum + 1

    # Finished receiving
    print("Done receiving")
    file.close()
    connection.close()