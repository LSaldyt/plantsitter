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
