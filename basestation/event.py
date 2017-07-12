'''
Event evaluator evaluates whether an event occurs in an image sequence
'''

class Event(object):
    def __init__(self, time, snap_url):
        self.time = time
        self.snap_url = snap_url

class MotionDetector(object):

    def __init__(self):
        self.count = 0

    # Execute motion detector on snap
    def execute(self, snap):

        # TODO: step motion detection algorithm
        self.count += 1
        if self.count%10:
            print('count: ' + str(self.count))
            return False
        else:
            # Event has occured
            print('Event occured')
            return True



class Check(object):

    def __init__(self):
        self.detector = MotionDetector()

    # Executes event check on snap
    def execute(self, snap):

        # Checks if event criteria has been met
        if self.detector.execute(snap):

            # Create and return event
            return Event(snap.time, snap.url)
        else:
            return False