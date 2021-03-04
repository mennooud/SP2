from pymongo import MongoClient

import MongoDB
import PGAdmin

client = MongoClient()
db = client.huwebshop
collection = db.products

items = MongoDB.getitems(collection)
