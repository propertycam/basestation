'''
Client sends data to basestation server
'''

import socket
import os
import time

# Connect the socket to the port where the server is listening
server_address = ('localhost', 50000)


# Open example image
#f = open('to_send.jpg','rb')

# Iterate over sample snaps
for filename in sorted(os.listdir('sample_snaps')):

    # Open sample snap
    print("sending snap: " + filename)
    f = open('sample_snaps/' + filename,'rb')

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)

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
    #sock.shutdown(socket.SHUT_RDWR)
    #sock.close()

    # Sleep thread to simulate 1 fps acquisition
    time.sleep(1)

print('Done sending')
