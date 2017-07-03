'''
Basestation recieves photos captured by propertycam camera units.
'''

import socket
import datetime

from basestation.datastore import DataStore
from basestation.snap import Snap
from basestation.snappipeline import SnapPipeline


# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to a port
#server_address = ('localhost', 50000)
server_address = ('', 50000)
sock.bind(server_address)
sock.listen()
print('Propertycam basestation listening on %s port %s' % server_address)

# TODO: Wait for cameras to connect

# Add connected cameras to datastore
ds = DataStore()
camera_mac_address = '001122334455'
ds.add_camera(camera_mac_address)

# Create snap processing pipeline
snap_pipeline = SnapPipeline(ds)

# Continuously accept and handle connections
while True:

    # Wait for connection
    connection, client_addr = sock.accept()
    print('Connection from ', client_addr)

    # TODO: Get camera MAC address and snap time from camera
    camera_mac_address = '001122334455'
    snap_time = datetime.datetime.now()

    # Receive snap parts and store in buffer
    snap_buffer = bytes()
    part_size = 1024
    part_buffer = connection.recv(part_size)
    partnum = 1
    while(part_buffer):
        #print('Recieved part ', partnum)
        snap_buffer += part_buffer
        part_buffer = connection.recv(part_size)
        partnum = partnum + 1

    # Finished receiving
    print("Done receiving")
    connection.close()

    # Execute snap pipeline
    snap = Snap(camera_mac_address, snap_time, snap_buffer)
    snap_pipeline.execute(snap)

    # Insert snap in database
    # snap = {"src" : relative_path_to_snapfile,
    #         "createdAt": snaptime }
    # result = db.snaps.insert_one(snap)
    # #print("Inserted snap id  " + str(result.inserted_id))
    #
    # # Update cameras last snap
    # db.cameras.update_one({'macaddress': camera.macaddress}, {'$set': {'lastsnap': relative_path_to_snapfile}})
