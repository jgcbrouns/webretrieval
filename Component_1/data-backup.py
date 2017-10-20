import sqlite3, re, operator, math, json, sys
from nltk.corpus import stopwords
import pandas as pd
from authentication import *

db = get_db()

### if "True", recomputes the tf and df and writes to MongoDB - change when document data has been changed
reindex = False

### Variables ###
DID = 'id'
TOP_N = 10
LIMIT_WORD_TF = 0 # How many times word has to appear in Tf to store it in the database

def prepare(text):
    stop = set(stopwords.words('english'))
    text = re.sub(r'[^\w]', ' ', text)
    text = re.sub(r'\b\w{1,1}\b', '', text)
    return [i for i in text.lower().split() if i not in stop]

def calculate(keywords, limit):
    count = {}
    for key in keywords:
        if key in count:
            count[key] += 1
        else:
            count[key] = 1
    for key in keywords:
        if count[key] <= limit:
            del count[key]
    return count

def sort(array, desc = True):
    return sorted(array.items(), key=operator.itemgetter(1), reverse=desc)

def idf(df, key, N):
    if key in df:
        return 1 + math.log10(N/df[key])
    return 1 + math.log10(N)

def normalizeTf(tf, did):
    for key in tf[did].keys():
        tf[did][key] /= len(tf[did]) * 1.0

def cosine_similarity(tfIdf, qTfIdf, DF, COUNT):
    dot_product = 0
    query_sc = 0;
    document_sc = 0;

    for qToken in qTfIdf:
        if qToken in tfIdf:
            dot_product += qTfIdf[qToken] * tfIdf[qToken]
            document_sc += math.pow(tfIdf[qToken], 2)
        else:
            dot_product += qTfIdf[qToken] * 0.0001 * idf(DF, qToken, COUNT)
            document_sc += math.pow(0.0001 * idf(DF, qToken, COUNT), 2)
        query_sc += math.pow(qTfIdf[qToken], 2)

    for token in tfIdf:
        if not token in qTfIdf:
            dot_product += tfIdf[token] * 0.0001 * idf(DF, token, COUNT)
            document_sc += math.pow(tfIdf[token], 2)

    if not query_sc or not document_sc:
        return 0

    cosine_similarity = dot_product / ( math.sqrt(query_sc) * math.sqrt(document_sc) )
    return cosine_similarity

def test_cosine_similarity(tfIdf, qTfIdf, DF, COUNT):
    dot_product = 0
    query_sc = 0;
    document_sc = 0;

    for qToken in qTfIdf:
        if qToken in tfIdf:
            dot_product += qTfIdf[qToken] * tfIdf[qToken]
            document_sc += math.pow(tfIdf[qToken], 2)
        else:
            dot_product += qTfIdf[qToken] * 0.0001 * idf(DF, qToken, COUNT)
            document_sc += math.pow(0.0001 * idf(DF, qToken, COUNT), 2)
        query_sc += math.pow(qTfIdf[qToken], 2)

    if not query_sc or not document_sc:
        return 0

    print qTfIdf
    print

    cosine_similarity = dot_product / ( math.sqrt(query_sc) * math.sqrt(document_sc) )
    return cosine_similarity

def topN(dic, n):
    top = sorted(dic, key=dic.get, reverse=True)
    return top[:n]


class DBInt:

    LIMIT = 2000
    ANAL_FIELD = "title" # Field name in the paper document
    anal_field = "title" # Field name in the database
    collection = "index_" + anal_field
    collection_df = collection + "_df"

    def __init__(self):
        self

    def add_bulk_tf(self, documentId, tokens):
        tf = {}
        for key in tokens:
            tf[key] = tokens[key] 
        db[collection].insert({'documentId' : documentId, 'data' : tf})

    def add_bulk_df(self, df):
        list_df = []
        for key in df:
            list_df.append({"keyword": key, "count": df[key]})
        db[collection_df].insert_many(list_df)

    def get_tf(self, documentId):
        return db[collection].find_one({'documentId': documentId});

    def get_all_tf(self):
        tf = {}
        for document in db[collection].find():
            tf[document['documentId']] = document['data']
        return tf

    def get_df(self):
        df = {}
        for item in db[collection_df].find():
            df[item['keyword']] = item['count']
        return df

    def get_document(self, documentId):
        return db.papers.find_one({'id': documentId});

    def get_documents(self, n):
        return list(db.papers.find({}, {"id" : 1, "title" : 1, "_id" : 0}).limit(n));

    def printJson(self, obj):
        print json.dumps(obj, indent=4, sort_keys=True)




    if reindex:
        print "Recompute the index"
        db[collection].remove({})
        db[collection_df].remove({})

        DOCUMENTS = get_documents(LIMIT)

        df = {}
        for document in DOCUMENTS:
            tokens = prepare(document[ANAL_FIELD])
            tokens = calculate(tokens, LIMIT_WORD_TF)
            print tokens
            add_bulk_tf(document[DID], tokens)
            for token in tokens:
                if token in df:
                    df[token] += 1
                else:
                    df[token] = 1
        add_bulk_df(df)
        

    tf = get_all_tf()
    DF = get_df()
    COUNT = len(tf)

    for key in tf.keys():
        normalizeTf(tf, key)

    tfIdf = {}

    for document in tf.keys():
        tfIdf[document] = {}
        for token in tf[document]:
            tfIdf[document][token] = tf[document][token] * idf(DF, token, COUNT)

    query = "I love neural network network"
    qTokens = prepare(query)
    qTf = calculate(qTokens, 0)
    qDf = {}
    for token in qTokens:
        if token in DF.keys():
            qDf[token] = DF[token]
        else:
            qDf[token] = 0

    for key in qTf.keys():
        qTf[key] /= len(qTf)*1.0

    qTfIdf = {}
    for token in qTf:
        qTfIdf[token] = qTf[token] * idf(DF, token, COUNT)

    cos_sim = {}
    for document in tf:
        cos_sim[document] = cosine_similarity(tfIdf[document], qTfIdf, DF, COUNT)

    top_documents  = topN(cos_sim, TOP_N)

    print
    print query
    print

    for d_id in top_documents:
        # print cos_sim[d_id]
        # print tfIdf[d_id]
        print get_document(d_id)['title'] + ' = ' + str(get_document(d_id)['id'])

    for document in top_documents:
        cos_sim[document] = test_cosine_similarity(tfIdf[document], qTfIdf, DF, COUNT)

    printJson(qTfIdf)