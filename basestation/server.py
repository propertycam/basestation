'''
Basestation recieves photos captured by propertycam camera units.
'''

import socket
import os
from pymongo import MongoClient
import datetime
import json

from basestation.camera import Camera


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

# Set directory to store snaps
webpublicdir = '/home/damon/propertycam/basestation-ui/public'

# Create directory to store snaps
#snapdir = 'snaps'
#if not os.path.exists(snapdir):
#    os.mkdir(snapdir)

# Connect to Meteor's Mongo Database
mongo_client = MongoClient('mongodb://localhost:3001/meteor')
db = mongo_client.meteor
#dbs = mongo_client.database_names()
#print(dbs)

# Initialize camera info in database
cameras = []
cameras.append(Camera('001122334455'))
c = cameras[0]
db.cameras.insert_one(c.__dict__)


# Continuously accept and handle connections
while True:

    # Wait for connection
    connection, client_addr = sock.accept()
    print('Connection from ', client_addr)

    # TODO: Get camera id (could use MAC address) and snap time from camera
    cam_id = '001122334455'
    snaptime = datetime.datetime.now()

    # Create directory to store camera snaps
    date = snaptime.strftime("%Y-%m-%d")
    snapdir = 'snaps/' + cam_id + '/' + date
    fullsnapdir = webpublicdir + '/' + snapdir
    if not os.path.exists(fullsnapdir):
        os.makedirs(fullsnapdir)

    # Write camera snap to file
    snapfile = snaptime.strftime("%H%M%S.%f") + '.jpg'
    relative_path_to_snapfile = snapdir +'/' + snapfile
    fullpathtosnapfile = fullsnapdir + '/' + snapfile
    file = open(fullpathtosnapfile, 'wb')

    # Create file to write snapshot to
#    snapnum = snapnum + 1
#    filename = str(snapnum).zfill(5) + '.jpg'
#    filepath = fullsnapdir + '/' + filename
#    file = open(filepath, 'wb')

    # Receive parts
    buffer_size = 1024
    buffer = connection.recv(buffer_size)
    partnum = 1
    while(buffer):
        #print('Recieved part ', partnum)
        file.write(buffer)
        buffer = connection.recv(buffer_size)
        partnum = partnum + 1

    # Finished receiving
    print("Done receiving")
    file.close()
    connection.close()

    # Insert snap in Mongo db
    snap = {"src" : relative_path_to_snapfile,
            "createdAt": snaptime }
    snap_id = db.snaps.insert_one(snap)
    print("Inserted snap id  " + str(snap_id))