'''
Snap processing pipeline
'''

from basestation.datastore import DataStore



class SnapPipeline(object):

    def __init__(self):
        # Create datastore
        self.datastore = DataStore()


    def execute(self, snap):

        # Add snap to the data store
        self.datastore.add_snap(snap)

        # Run event detector on snap

        # Store detected event
