'''
Snap processing pipeline
'''

import os
import shutil
from pymongo import MongoClient

class DataStore(object):

    def __init__(self):

        # Set root directory for file storage
        self.rootdir = '/home/damon/propertycam/basestation-ui/public'

        # Connect to Meteor's Mongo Database
        mongo_client = MongoClient('mongodb://localhost:3001/meteor')
        self.db = mongo_client.meteor

    # Adds snap to datastore
    # 1. saves snap to file and
    # 2. sets last snap of camera view
    def add_snap(self, snap):

        # Create directory to store camera snaps
        date = snap.time.strftime("%Y-%m-%d")
        snapdir = 'snaps/' + snap.cam_mac_address + '/' + date
        fullsnapdir = self.rootdir + '/' + snapdir
        if not os.path.exists(fullsnapdir):
            os.makedirs(fullsnapdir)

        # Write snap to file
        snapfile = snap.time.strftime("%H%M%S.%f") + '.jpg'
        fullpathtosnapfile = fullsnapdir + '/' + snapfile
        file = open(fullpathtosnapfile, 'wb')
        file.write(snap.buffer)
        file.close()

        # Copy to last snap file
        srcfile = fullpathtosnapfile;
        dstfile = self.rootdir + '/snaps/' + snap.cam_mac_address + '/lastsnap.jpg'
        shutil.copyfile(srcfile, dstfile)

        # Set lastsnap of camera view
        relative_path_to_snapfile = snapdir + '/' + snapfile
        #self.db.cameras.update_one({'macaddress': snap.cam_mac_address}, {'$set': {'lastsnap': relative_path_to_snapfile}}, upsert=True)

    def add_camera(self, camera_mac_address):
        if(self.db.cameras.find_one({"macaddress": camera_mac_address})):
            print("Camera allready in database")
        else:
            srcfile = self.rootdir + "/snaps/default.jpg"
            dstfile = self.rootdir + "/snaps/" + camera_mac_address + "/lastsnap.jpg"
            shutil.copyfile(srcfile, dstfile)
            cam_json = {"macaddress" : camera_mac_address,
                    "lastsnap" : "snaps/" + camera_mac_address + "/lastsnap.jpg"}
            self.db.cameras.insert_one(cam_json)