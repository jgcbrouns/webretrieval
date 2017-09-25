def get_db():

    #Insert the pymongo library so we can talk to mongoDB via our driver
    from pymongo import MongoClient

    #Connect to db and authenticate
    client = MongoClient('109.238.10.185', 27000)
    db = client['webretrieval']
    db.authenticate('webretrieval', 'tue')

    #Return a database instance
    return db

