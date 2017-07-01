class Camera(object):

    def __init__(self, macaddress, lastsnap='snaps/default.jpg'):
        self.macaddress = macaddress
        self.lastsnap = lastsnap