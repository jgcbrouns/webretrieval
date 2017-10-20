import sqlite3, operator
import networkx as nx
import matplotlib.pyplot as plt
import sys, progressbar

from repository import *
from authentication import *

'''
Author:         Jeroen Brouns
Description:    A script that migrates the sqlite to mongoDB
'''


class Data():

    @staticmethod
    def retrieve_data(input_file):
        conn = sqlite3.connect(input_file)
        c = conn.cursor()
        # query = 'SELECT a.name author, COUNT(DISTINCT p.Id) num_papers FROM authors a INNER JOIN paper_authors pa ON a.id=pa.author_id INNER JOIN papers p ON pa.paper_id=p.id WHERE year=2016 GROUP BY a.name ORDER BY COUNT(DISTINCT p.Id) DESC LIMIT 100'
        query = 'SELECT * FROM paper_authors'
        # ORDER BY id DESC LIMIT ' + str(n)
        query = c.execute(query).fetchall()
        return query


if __name__ == "__main__":

    # Get the database context
    db = get_db()

    documents = Data.retrieve_data('data/database.sqlite')
    titleCounter = 0
    
    # Initialize a progressbar
    bar = progressbar.ProgressBar(maxval=len(documents)).start()

    for document in documents:
        id = document[0]
        paper_id = document[1]
        author_id = document[2]

        add_paper_author(db, id, paper_id, author_id)

        # Update statusbar
        titleCounter = titleCounter + 1
        bar.update(titleCounter)


    

