import sqlite3, operator
import networkx as nx
import matplotlib.pyplot as plt

from repository import *
from authentication import *

'''
Author:         Jeroen Brouns
Description:    Applies PageRanking algorithm and exports results to db
'''


if __name__ == "__main__":

    # Get the database context
    db = get_db()

    cursor = get_references(db)

    G=nx.Graph()

    for document in cursor:
        documentId = document['documentId']
        G.add_node(documentId)
    
        for documentTuple in document['references_found']:
            
            documentTuple = documentTuple['documents'][1:-1]
            docList = documentTuple.strip().split(", ")
            
            for docId in docList:
                G.add_edge(documentId,docId)

    pr = nx.pagerank(G, alpha=0.9)
    #print pr

    for documentId in pr:
        pagerank = pr[documentId]
        add_pagerank(db, documentId, pagerank)
    

