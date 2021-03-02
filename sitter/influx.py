from influxdb import InfluxDBClient
from datetime import datetime

from config import Config

class SeriesDatabase:
    def __init__(self):
        self.config = Config()
        self.client = InfluxDBClient(host=self.config.plantsitter_influx_addr, 
                                     port=self.config.plantsitter_influx_port)
        self.client.drop_database(self.config.plantsitter_db)
        self.client.create_database(self.config.plantsitter_db)
        self.client.switch_database(self.config.plantsitter_db)

    def wrap(self, chunk, measurement='plant_telemetry', tags=None):
        if tags is None:
            tags = dict(source='piB')
        return dict(measurement=measurement,
                    tags=tags,
                    time=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    fields=chunk)

    def insert(self, data):
        if isinstance(data, list):
            data = [self.wrap(chunk) for chunk in data]
        else:
            data = [self.wrap(data)]
        print(data)
        self.client.write_points(data)

    def get(self, field):
        return self.client.query(f'SELECT "{field}" FROM "{self.config.plantsitter_db}"."autogen"."plant_telemetry"')
