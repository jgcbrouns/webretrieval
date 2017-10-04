import sqlite3, re, operator, math, string, unicodedata
from repository import *
from authentication import *

class Data():

    @staticmethod
    def retrieve_data(input_file, n):
        conn = sqlite3.connect(input_file)
        c = conn.cursor()
        # query = 'SELECT a.name author, COUNT(DISTINCT p.Id) num_papers FROM authors a INNER JOIN paper_authors pa ON a.id=pa.author_id INNER JOIN papers p ON pa.paper_id=p.id WHERE year=2016 GROUP BY a.name ORDER BY COUNT(DISTINCT p.Id) DESC LIMIT 100'
        query = 'SELECT * FROM papers'
        # ORDER BY id DESC LIMIT ' + str(n)
        query = c.execute(query).fetchall()
        return query

    @staticmethod
    def retrieve_titles(input_file, n):
        conn = sqlite3.connect(input_file)
        c = conn.cursor()
        #query = 'SELECT a.name papers a INNER JOIN paper_authors pa ON a.id=pa.author_id INNER JOIN papers p ON pa.paper_id=p.id WHERE year=2016 GROUP BY a.name ORDER BY COUNT(DISTINCT p.Id) DESC LIMIT 100'
        query = 'SELECT title,id FROM papers ORDER BY id DESC LIMIT ' + str(n)
        query = c.execute(query).fetchall()
        return query


    @staticmethod
    def prepare(text):
        stop = set(stopwords.words('english'))
        text = re.sub(r'[^\w]', ' ', text)
        return [i for i in text.lower().split() if i not in stop]


if __name__ == "__main__":

    db = get_db()

    titles = Data.retrieve_titles('data/database.sqlite', 6500)
    documents = Data.retrieve_data('data/database.sqlite', 6500)

    # titles = Data.tosequence(titles)

    for title in list(reversed(titles)):
        titleId = title[1]
        amountOfWordsInTitle = len(title[0].split())
        
        if amountOfWordsInTitle > 3:

            print "Looking for title: " + str(title[0])
            wordListForTitle = re.sub("[^\w]", " ",  title[0]).split()
            str1 = ' '.join(wordListForTitle)

            goodTitle = title[0]
            referencesList = []

            for document in documents:

                filter = "References"
                if filter in str(document[6]):
                    referencesText = ((str(document[6])).split(filter,1)[1])

                    documentId = document[0]

                    if goodTitle in str(referencesText):
                        
                        if documentId != titleId:
                            referencesList.append(documentId);
                            print "true"
                        # elif documentId == titleId:
                        #     print "SELFREFERENCE"

            if referencesList:
                add_reference_for_title(db, goodTitle, referencesList, titleId)   





 