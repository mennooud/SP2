

def getitems(collection, sortterm=False):
    if sortterm:
        return collection.find().sort(sortterm)
    return collection.find()