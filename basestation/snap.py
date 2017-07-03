'''
Snap class
'''

class Snap(object):
    def __init__(self, cam_mac_address, time, buffer ):
        self.cam_mac_address = cam_mac_address
        self.time = time
        self.buffer = buffer
