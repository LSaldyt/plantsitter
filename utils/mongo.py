from pymongo import MongoClient

client = MongoClient()
print(client)
database   = client.example
collection = database.example
print(collection)
print(dir(collection))
result = collection.insert_one(dict(test='this!', l=['these','these'], n=0))
print(result)
print(result.inserted_id)
result = collection.insert_many([dict(test='this!', l=['these','these'], n=0)])
print(collection.find())
print(collection.find_one(dict(test='this!')))
from influxdb import InfluxDBClient
from datetime import datetime

from utils.config import Config

class MongoDatabases:
    def __init__(self, databases):
        self.config = Config()
        self.client = MongoClient() # self.config.mongo_addr, self.config.mongo_port

        # Clear existing databases
        for database in databases:
            self.client.drop_database(database)

    def __getattr__(self, name):
        try:
            if hasattr(self, name):
                assert not hasattr(self.client, name), f'The name {name} is shared between MongoDatabase class and a database name'
                return object.__getattr__(self, name)
            else:
                return getattr(self.client, name)
        except KeyError:
            return object.__getattr__(self, name)
