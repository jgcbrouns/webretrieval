
import pymongo
import pprint
import pickle


# reload stored data
with open('AuthorID_Value_KEYWORDS.pickle', 'rb') as handle:
    Authorid_Score_keywords_list = pickle.load(handle)


def get_db():

    #Insert the pymongo library so we can talk to mongoDB via our driver
    from pymongo import MongoClient

    #Connect to db and authenticate
    client = MongoClient('109.238.10.185', 27000)
    db = client['webretrieval']
    db.authenticate('webretrieval', 'tue')

    #Return a database instance
    return db

db = get_db()


def add_Authorid_Score_keywords(db, authorid, Score, keywords):
    db.Authorid_Score_keywords.insert(
        {'author_id': authorid, 'Score': Score, 'keywords': keywords }
    )


for items in Authorid_Score_keywords_list:
    add_Authorid_Score_keywords(db, items[0], items[1], items[2:])

