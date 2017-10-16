import sqlite3, re, operator, math, json, sys
from nltk.corpus import stopwords
import pandas as pd

# ---- some extra ideas for parsing: ----
# - remove one character words
# - check if only one letter differs
# Global class for DF, locals for tf
# add most descriptive top 5 tf-idf to the cosine similarity
# add vectors to mongo for optimization
class Data():

    @staticmethod
    def retrieve_data(input_file, did, fields, limit):
        dataframe = pd.read_csv(input_file, usecols=fields + [did])
        result = {}
        # conn = sqlite3.connect(input_file)
        # c = conn.cursor()
        # query = 'SELECT a.name author, COUNT(DISTINCT p.Id) num_papers FROM authors a INNER JOIN paper_authors pa ON a.id=pa.author_id INNER JOIN papers p ON pa.paper_id=p.id WHERE year=2016 GROUP BY a.name ORDER BY COUNT(DISTINCT p.Id) DESC LIMIT 100'
        # query = 'SELECT * FROM papers ORDER BY id DESC LIMIT ' + str(n)
        # query = c.execute(query)
        i = 0
        for index,row in dataframe.iterrows():
            dic = {}
            for field in fields:
                dic[field] = row[field]
            result[row[did]] = dic
            i += 1
            if i >= limit:
                break
        return result

    @staticmethod
    def prepare(text):
        stop = set(stopwords.words('english'))
        text = re.sub(r'[^\w]', ' ', text)
        text = re.sub(r'\b\w{1,1}\b', '', text)
        return [i for i in text.lower().split() if i not in stop]

    @staticmethod
    def calculate(keywords):
        count = {}
        for key in keywords:
            if key in count:
                count[key] += 1
            else:
                count[key] = 1
        return count

    @staticmethod
    def sort(array, desc = True):
        return sorted(array.items(), key=operator.itemgetter(1), reverse=desc)

    @staticmethod
    def concat_counts(counts):
        df = {}
        for count in counts.values():
            for key in count:
                if key in df:
                    df[key] += 1
                else:
                    df[key] = 1
        return df

    @staticmethod
    def idf(df, key, N):
        if key in df:
            return 1 + math.log10(N/df[key])
        return 1 + math.log10(N)

    @staticmethod
    def normalizeTf(tf, did):
        for key in tf[did].keys():
            tf[did][key] /= len(tf[did]) * 1.0

    # @staticmethod
    # def tfIdf(tf, idf):

    @staticmethod
    def cosineSimilarity(query):
        return Data.prepare(query)

    @staticmethod
    def compute_similarity(tfIdf, qTfIdf):
        dot_product = 0
        query_sc = 0;
        document_sc = 0;

        for qToken in qTfIdf:
            if qToken in tfIdf:
                dot_product += qTfIdf[qToken] * tfIdf[qToken]
                document_sc += math.pow(tfIdf[qToken], 2)
            query_sc += math.pow(qTfIdf[qToken], 2)

        if not query_sc or not document_sc:
            return 0

        cosine_similarity = dot_product / ( math.sqrt(query_sc) * math.sqrt(document_sc) )
        return cosine_similarity

    @staticmethod
    def topN(dic, n):
        top = sorted(dic, key=dic.get, reverse=True)
        return top[:n]

if __name__ == "__main__":

    def printJson(obj):
        i = 1
        # print json.dumps(obj, indent=4, sort_keys=True)

    ### Variables ###
    did = 'id'
    anal_field = 'paper_text'
    fields = [anal_field, 'title', 'year']
    limit = 10

    documents = Data.retrieve_data('../data/papers.csv', did, fields, limit)
    N = len(documents)

    printJson(documents)

    tf = {}
    for document in documents.items():
        tokens = Data.prepare(document[1][anal_field])
        # print tokens
        tf[document[0]] = Data.calculate(tokens)
        print Data.sort(tf[document[0]])
    printJson(tf)

    for key in tf.keys():
        Data.normalizeTf(tf, key)

    printJson(tf)

    df = Data.concat_counts(tf)
    printJson(df)

    tfIdf = {}

    for document in documents.items():
        tfIdf[document[0]] = {}
        tokens = Data.prepare(document[1][anal_field])
        for token in tokens:
            tfIdf[document[0]][token] = tf[document[0]][token] * Data.idf(df, token, N)

    printJson(tfIdf)

    query = "I love neural network network"
    qTokens = Data.prepare(query)
    qTf = Data.calculate(qTokens)
    qDf = {}
    for token in qTokens:
        if token in df.keys():
            qDf[token] = df[token]
        else:
            qDf[token] = 0

    for key in qTf.keys():
        qTf[key] /= len(qTf)*1.0

    qTfIdf = {}
    for token in qTokens:
        qTfIdf[token] = qTf[token] * Data.idf(df, token, N)
    
    printJson(qTfIdf)

    cos_sim = {}
    for document in documents.items():
        # print document[0]
        printJson(tfIdf[document[0]])
        cos_sim[document[0]] = Data.compute_similarity(tfIdf[document[0]], qTfIdf)

    printJson(cos_sim)
    printJson(Data.topN(cos_sim, 4))

    top_documents  = Data.topN(cos_sim, 10)

    print
    print query
    print

    for d_id in top_documents:
        print documents[d_id]['title'] + ' = ' + str(documents[d_id]['year'])

    printJson(qTfIdf)

    # for text in texts:
    #     tokens = Data.prepare(text[6])
    #     count  = Data.calculate(tokens)
    #     tf[text[0]] = count
    # df = Data.concat_counts(tf)
    # for key in tf.keys():
    #     Data.normalizeTf(tf, key)


    # sort_df = Data.sort(df, False)
    #print(tf)
