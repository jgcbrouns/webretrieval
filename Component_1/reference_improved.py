import sqlite3, re, operator, math, string, unicodedata, time, sys, progressbar
from repository import *
from authentication import *

'''
Author:         Jeroen Brouns
Description:    Foreach document(title), finds which other documents refer to it.
Runtime:        (6500 documents and titles): 63 minutes
'''

class Data():

    @staticmethod
    def retrieve_data(input_file):
        conn = sqlite3.connect(input_file)
        c = conn.cursor()
        # query = 'SELECT a.name author, COUNT(DISTINCT p.Id) num_papers FROM authors a INNER JOIN paper_authors pa ON a.id=pa.author_id INNER JOIN papers p ON pa.paper_id=p.id WHERE year=2016 GROUP BY a.name ORDER BY COUNT(DISTINCT p.Id) DESC LIMIT 100'
        query = 'SELECT * FROM papers'
        # ORDER BY id DESC LIMIT ' + str(n)
        query = c.execute(query).fetchall()
        return query

    @staticmethod
    def retrieve_titles(input_file):
        conn = sqlite3.connect(input_file)
        c = conn.cursor()
        #query = 'SELECT a.name papers a INNER JOIN paper_authors pa ON a.id=pa.author_id INNER JOIN papers p ON pa.paper_id=p.id WHERE year=2016 GROUP BY a.name ORDER BY COUNT(DISTINCT p.Id) DESC LIMIT 100'
        query = 'SELECT title,id FROM papers'
        query = c.execute(query).fetchall()
        return query


    @staticmethod
    def prepare(text):
        stop = set(stopwords.words('english'))
        text = re.sub(r'[^\w]', ' ', text)
        return [i for i in text.lower().split() if i not in stop]


if __name__ == "__main__":

    # Get the database context
    db = get_db()

    # Retrieve queryresults for titles and documents as lists
    titles = Data.retrieve_titles('data/database.sqlite')
    documents = Data.retrieve_data('data/database.sqlite')

    # Initialize a progressbar
    bar = progressbar.ProgressBar(maxval=len(titles)).start()

    # Variable for counting how many titles are processed (fed into progressbar)
    titleCounter = 0

    for title in list(reversed(titles)):
        titleId = title[1]
        amountOfWordsInTitle = len(title[0].split())
        
        # Check if title has more than 3 words, if so; look for references
        # Note: we do not allow titles with less than 3 words, since it often is not unique enough:
        #       (it might not be an actual reference, but just random found text)
        if amountOfWordsInTitle > 3:

            # Setting some variables
            goodTitle = title[0].lower()
            referencesList = []

            # Foreach document, search if title occurs as a reference
            for document in documents:

                referencesText = str(document[6].lower())
                documentId = document[0]

                if goodTitle in str(referencesText):
                    
                    # If the found document is different from the document which title we are searching for
                    if documentId != titleId:
                        referencesList.append(documentId);
                        #print "true"
                    # elif documentId == titleId:
                    #     print "SELFREFERENCE"

            # If we found references, add to database
            if referencesList:
                add_reference_for_title(db, goodTitle, referencesList, titleId)   

        # Update statusbar
        titleCounter = titleCounter + 1
        bar.update(titleCounter)




 