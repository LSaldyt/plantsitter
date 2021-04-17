import patch

import dash_devices

from time      import time
from pprint    import pprint

import logging as log

from .monitor import Monitor

class Sitter(Monitor):
    def __init__(self, app, connections, mongo):
        Monitor.__init__(self, app, connections)
        self.mongo = mongo

    def update(self, telem):
        Monitor.update(self, telem)

        for plant in self.mongo.plants.list.find():
            print(plant)

