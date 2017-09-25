
# m.py

def get_db():
    from pymongo import MongoClient

    client = MongoClient('109.238.10.185', 27000)
    db = client['webretrieval']
    db.authenticate('webretrieval', 'tue')

    return db

