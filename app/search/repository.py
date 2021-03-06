import sys,ast
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


def get_author(db, author_id):
    author = db.authors.find_one({'author_id': author_id })
    return author   

def get_papers_for_intquery(db, year):
    cursor = db.pages.find({'year': int(year) })
    return cursor

def get_keywords_for_paper(db, paper_id):
    author = db.Paperid_keywords_V1.find_one({'paper_id': paper_id })
    return author  

def get_author_topic_information(db, author_id):
    # author_id gets converted to string because people dont know difference between string and int
    cursor = db.author_id_topic.find_one({'author_id': str(author_id) })
    return cursor   

def get_authors_for_paper(db, documentId):
    cursor = db.paper_authors.find({'paper_id': documentId })
    authorsList = []
    for author in cursor:
        author = get_author(db,author['author_id'])
        authorName = author['name']
        authorId = author['author_id']
        jsonInstance = {'name': authorName,'id': authorId}
        authorsList.append(jsonInstance)
    return authorsList

def get_references_for_paper(db, documentId):
    cursor = db.title_references.find_one({'documentId': int(documentId) })
    referencesList = []
    referencesFound = cursor['references_found']
    print >>sys.stderr, 'References:' 
    for reference in referencesFound:
        references = reference['documents']
        references = ast.literal_eval(references)

        for documentId in references:
            paper = get_paper(db, documentId)
            title = paper['title']
            year = paper['year']
            authorsList = get_authors_for_paper(db, documentId)
            
            jsonInstance = {'title': title,'documentId': documentId, 'year': year, 'authors': authorsList}
            referencesList.append(jsonInstance)
            print >>sys.stderr, referencesList

    return referencesList   
        
   