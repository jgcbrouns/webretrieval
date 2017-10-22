import sqlite3, re, operator, math, json, sys
from nltk.corpus import stopwords
from authentication import *


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

def topN(dic, n):
    top = sorted(dic, key=dic.get, reverse=True)
    return top[:n]

### if "True", recomputes the tf and df and writes to MongoDB - change when document data has been changed
reindex = False

### Variables ###
LIMIT_WORD_TF = 0 # How many times word has to appear in Tf to store it in the database

class DBHelper:

    LIMIT = 2000
    db = get_db()

    def __init__(self, anal_field, db_field):
        self.anal_field = anal_field
        self.db_field = db_field
        self.collection = "index_" + db_field
        self.collection_df = self.collection + "_df"

    def add_bulk_tf(self, documentId, tokens):
        tf = {}
        for key in tokens:
            tf[key] = tokens[key] 
        self.db[self.collection].insert({'documentId' : documentId, 'data' : tf})

    def add_bulk_df(self, df):
        list_df = []
        for key in df:
            list_df.append({"keyword": key, "count": df[key]})
        self.db[self.collection_df].insert_many(list_df)

    def get_tf(self, documentId):
        return self.db[self.collection].find_one({'documentId': documentId});

    def get_all_tf(self):
        tf = {}
        for document in self.db[self.collection].find():
            tf[document['documentId']] = document['data']
        return tf

    def get_df(self):
        df = {}
        for item in self.db[self.collection_df].find():
            df[item['keyword']] = item['count']
        return df

    def get_document(self, documentId):
        return self.db.pages.find_one({'documentId': documentId});

    def get_documents(self):
        return list(self.db.pages.find({}, {"documentId" : 1, self.anal_field : 1, "title" : 1, "_id" : 0}).limit(self.LIMIT));

    def clean_db(self):
        self.db[self.collection].remove({})
        self.db[self.collection_df].remove({})

    def printJson(obj):
        print json.dumps(obj, indent=4, sort_keys=True)

def final(query, top_n):

    ANAL_FIELD = "title"

    DBH = DBHelper(ANAL_FIELD, "title")

    if reindex:
        print "Recompute the index"
        DBH.clean_db()

        DOCUMENTS = DBH.get_documents()

        df = {}
        for document in DOCUMENTS:
            tokens = prepare(document[ANAL_FIELD])
            tokens = calculate(tokens, LIMIT_WORD_TF)
            DBH.add_bulk_tf(document['documentId'], tokens)
            for token in tokens:
                if token in df:
                    df[token] += 1
                else:
                    df[token] = 1
        DBH.add_bulk_df(df)
        

    tf = DBH.get_all_tf()
    DF = DBH.get_df()
    COUNT = len(tf)

    for key in tf.keys():
        normalizeTf(tf, key)

    tfIdf = {}

    for document in tf.keys():
        tfIdf[document] = {}
        for token in tf[document]:
            tfIdf[document][token] = tf[document][token] * idf(DF, token, COUNT)

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

    top_documents  = topN(cos_sim, top_n)

    return top_documents

    # for d_id in top_documents:
    #     print DBH.get_document(d_id)['title'] + ' = ' + str(DBH.get_document(d_id)['documentId'])

if __name__ == "__main__":
    print final("I love neural network network", 5)