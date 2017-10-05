import sqlite3, operator
import networkx as nx
import matplotlib.pyplot as plt

from repository import *
from authentication import *

'''
Author:         Jeroen Brouns
Description:    Applies PageRanking algorithm to created referencegraph and display top 10 in console

'''


if __name__ == "__main__":

    # Get the database context
    db = get_db()

    cursor = get_references(db)

    G=nx.Graph()
    count = 0
    for document in cursor:
        documentId = document['documentId']
        G.add_node(documentId)
    
        for documentTuple in document['references_found']:
            
            documentTuple = documentTuple['documents'][1:-1]
            docList = documentTuple.strip().split(", ")
            
            for docId in docList:
                count = count + 1
                
    print count

