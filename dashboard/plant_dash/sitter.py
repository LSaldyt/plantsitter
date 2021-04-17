import patch

import dash_devices

from time      import time
from pprint    import pprint

import logging as log

from .monitor import Monitor

from plant_care.plant_scraper import PlantScraper
self.scraper = PlantScraper(self.mongo)

class Sitter(Monitor):
    def __init__(self, app, connections, mongo):
        Monitor.__init__(self, app, connections)
        self.mongo = mongo

    def update(self, telem):
        Monitor.update(self, telem)

        for plant in self.mongo.plants.list.find():
            name   = plant['name']
            sensor = plant['sensor']
            x      = plant['x']
            y      = plant['y']

            try:
                moisture = telem[f'moisture_{sensor}']
            except KeyError:
                print(f'Sensor {sensor} not found')

            print(f'Plant {name} @ ({x}mm, {y}mm) has moisture {moisture} from sensor {sensor}')

