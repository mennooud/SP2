from pymongo import MongoClient

import MongoDB

client = MongoClient()
db = client.huwebshop
collection = db.products

items = MongoDB.getitems(collection)
for item in items[:10]:
    print(item)