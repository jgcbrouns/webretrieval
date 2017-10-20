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
    db.title_references2.update(
        { 'title': title, 'documentId': titleId },
        { '$push': {'references_found': {'documents': str(documentIdList)}}}, upsert=True, multi=True
    )


'''
    Gets all the references in the colleciton title_references
    @param db
'''
def get_references(db):
    cursor = db.title_references2.find({})
    return cursor

'''
    Returns title for a specific documentId
    @param db, documentId
'''
def get_title_for_document_id(db, documentId):
    cursor = db.title_references2.find_one({'documentId': documentId })
    return cursor


'''
    adds a pagerank value for a specific documentId
    @param db, pageRank, documentId
'''
def add_pagerank(db, documentId, pageRank):
    db.pagerank.insert(
        { 'documentId': documentId, 'PageRank': pageRank,  }
    )

def add_paper(db, id, year, title, event_type, pdf_name, abstract, paper_text):
    db.pages.insert(
        { 'documentId': id, 'year': year, 'title': title, 'event_type': event_type, 'pdf_name': pdf_name, 'abstract': abstract, 'paper_text': paper_text }
    )

def get_paper(db, documentId):
    cursor = db.pages.find_one({'documentId': documentId })
    return cursor

def add_paper_author(db, documentId, paper_id, author_id):
    db.paper_authors.insert({ 'documentId': documentId, 'paper_id': paper_id, 'author_id': author_id }
    )

def add_author(db, documentId, name):
    db.authors.insert({ 'author_id': documentId, 'name': name }
    )

def get_authors_for_paper(db, documentId):
    cursor = db.authors.find_one({'id': documentId })
    return cursor

