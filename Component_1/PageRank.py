import sqlite3, operator
import networkx as nx
import matplotlib.pyplot as plt

from repository import *
from authentication import *

'''
Author:         Jeroen Brouns
Description:    Applies PageRanking algorithm to created referencegraph

Result:

1. 2882 - Infinite latent feature models and the Indian buffet process - 0.00955888260995
2. 2979 - Efficient sparse coding algorithms - 0.00919983118033
3. 3749 - Locality-sensitive binary codes from shift-invariant kernels - 0.00262792779807
4. 2636 - Analysis of a greedy active learning strategy - 0.00346660254589
5. 3933 - Structured sparsity-inducing norms through submodular functions - 0.00383128278449
6. 3313 - Sparse deep belief net model for visual area V2 - 0.00413794006623
7. 1048 - Gaussian Processes for Regression - 0.00604755435219
8. 1967 - Partially labeled classification with Markov random walks - 0.0032591116382
9. 3325 - A general agnostic active learning algorithm - 0.00468939172506
10. 2943 - Coarse sample complexity bounds for active learning - 0.00465899146596

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

    top = dict(sorted(pr.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
    print top

    counter = 0
    for documentId in top:
        counter = counter + 1
        document = get_title_for_document_id(db,documentId)
        print (str(counter) + '. ' + str(documentId) + ' - ' + document['title']) + ' - ' + str(top[documentId])
    

