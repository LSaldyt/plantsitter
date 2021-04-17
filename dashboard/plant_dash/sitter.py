import patch

import dash_devices

from time      import time
from pprint    import pprint

import logging as log
import json

from .monitor import Monitor

from plant_care.plant_scraper import PlantScraper

'''
name : name
summary : wikipedia summary
latin_name : 'Agave americana'
common_name : ['Agave', 'American century plant']
habitat : 'Perennial'
height : 7.5,
hardiness : [8, 9, 10, 11]
growth : ['slow']
soil : ['light', 'medium']
shade : ['none']
moisture : ['dry', 'moist']
edible : 3
medicinal : 3
other : ' '
'''

# The following are watering thresholds
#   For example, dry plants are only watered if their moisture is 0.8 or more
calibrate = dict(dry=0.8,
                 moist=0.6,
                 wet=0.4,
                 water=0.2)

class Sitter(Monitor):
    def __init__(self, app, connections, mongo):
        Monitor.__init__(self, app, connections)
        self.mongo = mongo
        self.scraper = PlantScraper(self.mongo)


    def send(self, data):
        command = self.connections.get('command', None)
        if command is not None:
            command.send(json.dumps(data))
        else:
            log.info(f'Cannot send command: No connection!')

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
                moisture = 0.0 # Safe value, won't be watered!

            print(f'Plant {name} @ ({x}mm, {y}mm) has moisture {moisture} from sensor {sensor}')
            needs = list(self.scraper.care.find(dict(name=name)))[0]
            moist_req = calibrate[needs['moisture'][0]]
            print(f'Threshold: {moist_req}')
            if moist_req < moisture:
                status = 'needs to be watered'
                self.send(dict(water=True, x=x, y=y))
            else:
                status = 'is already watered'
            print(f'According to this, the {name} {status}')
