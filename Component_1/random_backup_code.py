

    #db.index_text.update({'keyword' : keyword, "data": {"$elemMatch": {"documentId": documentId}}}, {"$set": {"data.$.amount": 5}})
    #db.index_text.update({'keyword' : keyword, "data.documentId": documentId} , {"$set": {"data.$.amount": 5}})
    #db.index_text.update({"sessions.0.issues": {$elemMatch: {id: <yourValue>}}}, {$set: {"sessions.0.issues.$.text": "newText"}})
    #db.index_text.insert({"keyword": str(keyword), "data": [{"documentId": str(documentId), "amount": amount}]})


# {
#     "name" : "student_1",
#     "courses" : [
#         {
#             "name" : "Algebra",
#             "grades" : [ 98, 96, 92 ]
#         },
#         {
#             "name" : "Computers",
#             "grades" : [ 80 ]
#         }
#     ]
# }
#db.student.update({name:'student_1','courses.name':'Algebra'},{$inc:{"courses.$.grades.1":10}})
    #db.student.update({'keyword':keyword,'data.documentId': documentId},{"$inc":{"data.$.amount":5}})


    # db.index_text.update({
    #     "keyword": keyword,
    #     "data": {
    #         "$not": {
    #             "$elemMatch": {
    #                 str(documentId): amount
    #             }
    #         }
    #     }
    # }, {
    #     "keyword": keyword,
    #     "$addToSet": {
    #         "data": {
    #             str(documentId): amount
    #         }
    #     }
    # }, multi=False, upsert=True );

    # db.index_text.update({
    #     keyword: {
    #         "$not": {
    #             "$elemMatch": {
    #                 str(documentId): amount
    #             }
    #         }
    #     }
    # }, {
    #     "$addToSet": {
    #         keyword: {
    #             str(documentId): amount
    #         }
    #     }
    # }, multi=False, upsert=True );

# def add_country(db):
#     db.countries.insert({"name" : "Canada"})

# def get_country(db):
#     return db.countries.find_one()

# def say_hi(db):
#     return "test"
