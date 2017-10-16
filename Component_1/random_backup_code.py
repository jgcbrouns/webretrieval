

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


       # print titleFiltered
        # print type('Analysis of a greedy active learning strategy')
        # print unicode(str(title[0]))
        # wordListForTitle = re.sub("[^\w]", " ",  title[0]).split()
        # for word in wordListForTitle:
        #print title[0]
        #print "\n"
# 'Analysis of a greedy active learning strategy'


    # for title in titles:
    #     #print "Looking for title: " + str(title[0])
    #     wordListForTitle = re.sub("[^\w]", " ",  title[0]).split()
    #     # print "but actually looking for words:"
    #     # for titleWord in wordListForTitle:
    #     #     print titleWord
    #     for text in texts:
    #     # for part in text:
    #         # print "******************start**********************"
    #         # print text[6]
    #         # print "******************end**********************"
            
          
    #         if title[0] in text[6]:
    #             print "I found the title: " + str(title[0]) + " in: "
    #             print text[6]

            # filter = "References"
            # if filter in str(text):
            #     referencesText = ((str(text)).split(filter,1)[1])
           
            #     wordListForReferences = re.sub("[^\w]", " ",  referencesText).split()
                
            #     counter = 0
            #     for word in wordListForReferences:
            #         if word == wordListForTitle[counter]:

            #             counter = counter + 1
            #             if counter == 3:                              
            #                 print "I found the title: " + str(title[0]) + " in: "
            #                 print referencesText
            #                 counter = 0




       # for text in texts:
       #      tokens = Data.prepare(text[6])
       #      counter = 0
       #      for token in tokens:
       #          if token == wordListForTitle[counter]:
       #              counter = counter + 1
       #              if counter == 3:                              
       #                  print "I found the title: " + str(title[0]) + " in: "
       #                  print token
       #                  counter = 0


                   # filter = "References"
            # if filter in str(document[6]):
            #     referencesText = ((str(document[6])).split(filter,1)[1])
           
            #     wordListForReferences = re.sub("[^\w]", " ",  referencesText).split()
                
            #     counter = 0
            #     for word in wordListForReferences:
            #         if word == wordListForTitle[counter]:

            #             counter = counter + 1
            #             if counter == 5 || counter == len(wordListForTitle):                              
            #                 print "I found the title: " + str(title[0]) + " in: "
            #                 print referencesText
            #                 counter = 0
            #         else:
            #             counter = 0
