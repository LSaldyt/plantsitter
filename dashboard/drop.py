from pymongo import MongoClient

if __name__ == '__main__':
    c = MongoClient()
    c.plants.list.drop()

