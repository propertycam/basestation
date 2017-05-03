'''
Client sends data to basestation server
'''

import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 50000)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

# Open example image
f = open('to_send.jpg','rb')

# Send to basestation
buffer_size = 1024
buffer = f.read(buffer_size)
part_num = 1
while(buffer):
    print('Sending part ', part_num)
    sock.send(buffer)
    buffer = f.read(buffer_size)
    part_num = part_num + 1

# Finished sending
f.close()
print('Done sending')
sock.close()