'''
    adds an amount to the database for a specific keyword and documentId
    @param db, keyword, documentId, amount
'''
def add_amount(db, keyword, documentId, amount):
    db.index_text.update(
        { 'keyword': keyword,  },
        { '$push': {'data': {'documentId': str(documentId), 'amount': amount}}}, upsert=True
    )

'''
    removes ALL amount to the database for a specific keyword and documentId
    @param db, keyword, documentId, amount
'''
def remove_amount(db, keyword, documentId, amount):
    db.index_text.update(
        { 'keyword': keyword,  },
        { '$pull': {'data': {'documentId': str(documentId)}}}, upsert=True
    )

'''
    updates an amount to the database for a specific keyword and documentId
    @param db, keyword, documentId, amount
'''
def update_amount(db, keyword, documentId, amount):
    remove_amount(db, keyword, documentId, amount)
    add_amount(db, keyword, documentId, amount)


'''
    adds an amount to the database for a specific keyword and documentId
    @param db, keyword, documentId, amount
'''
def add_reference_for_title(db, title, documentIdList, titleId):
    db.title_references.update(
        { 'title': title,  },
        { 'titleId': titleId,  },
        { '$push': {'references_found': {'documents': str(documentIdList)}}}, upsert=True, multi=True
    )

