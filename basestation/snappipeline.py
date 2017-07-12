'''
Snap processing pipeline
'''

from basestation.datastore import DataStore
from basestation import event



class SnapPipeline(object):

    def __init__(self, datastore):

        # Create datastore
        self.datastore = datastore

        # Create event evaluator
        self.eventcheck = event.Check()


    def execute(self, snap):

        # Add snap to the data store
        self.datastore.add_snap(snap)

        # Run event check on snap
        event = self.eventcheck.execute(snap)

        # Store event if detected
        if(event):
            self.datastore.add_event(event)


