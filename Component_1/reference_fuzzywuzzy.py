import sqlite3, re, operator, math, string, unicodedata, time, sys, progressbar, nltk
from repository import *
from authentication import *
from nltk import tokenize
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

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

    # nltk.download('punkt')

    # Retrieve queryresults for titles and documents as lists
    titles = Data.retrieve_titles('data/database.sqlite')
    documents = Data.retrieve_data('data/database.sqlite')

    # Initialize a progressbar
    # bar = progressbar.ProgressBar(maxval=len(titles)).start()

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
            goodTitle = title[0]
            referencesList = []

            # Foreach document, search if title occurs as a reference
            for document in documents:

                # Filter on reference, when "Reference" occurs in text, continue with 
                # only the text from the point where "Reference" occurs
                filter = "References"
                if filter in str(document[6]):
                    referencesText = ((str(document[6])).split(filter,1)[1])

                    documentId = document[0]

                    sentencesList = tokenize.sent_tokenize(referencesText)

                    for sentence in sentencesList:

                        ratio = fuzz.ratio(goodTitle, sentence)

                        if ratio > 80:
                            print ("Title: "+goodTitle+" - Found: "+sentence+" - Ratio: "+str(ratio))




                    # if goodTitle in str(referencesText):
                        
                    #     # If the found document is different from the document which title we are searching for
                    #     if documentId != titleId:
                    #         referencesList.append(documentId);
                    #         #print "true"
                    #     # elif documentId == titleId:
                    #     #     print "SELFREFERENCE"

            # If we found references, add to database
        #     if referencesList:
        #         add_reference_for_title(db, goodTitle, referencesList, titleId)   

        # # Update statusbar
        # titleCounter = titleCounter + 1
        # bar.update(titleCounter)




 