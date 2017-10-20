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

'''
    Returns title for a specific documentId
    @param db, documentId
'''
def get_pagerank(db, documentId):
    cursor = db.pagerank.find_one({'documentId': documentId })
    return cursor

def get_topics_for_document(db, documentId):
    cursor = db.topic_distribution.find_one({'documentId': documentId })
    return cursor

def get_paper(db, documentId):
    cursor = db.pages.find_one({'documentId': documentId })
    return cursor

def add_paper_author(db, documentId, paper_id, author_id):
    db.paper_authors.insert(
        { 'documentId': documentId, 'paper_id': paper_id, 'author_id': author_id }
    )

def add_author(db, documentId, name):
    db.authors.insert(
        { 'author_id': documentId, 'name': name }
    )

def get_authors_for_paper(db, documentId):
    cursor = db.paper_authors.find({'documentId': documentId })
    authorsNameList = []
    for author in cursor:
        print >>sys.stderr, author

    # cursor = db.paper_authors.find_one({'documentId': documentId })

def get_authors_for_paper(db, documentId):
    cursor = db.authors.find_one({'id': documentId })
    return cursor

    
