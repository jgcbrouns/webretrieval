import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

from repository import *
from authentication import *

'''
Author:         Jeroen Brouns
Description:    Creates directed graph from documentreferences such that: 
                Nodes = document
                Edges = Reference from node A to node B
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
                    

    nx.draw(G, node_size=10)
    #nx.draw(G)
    plt.savefig("simple_path.png") # save as png
    plt.show() # display