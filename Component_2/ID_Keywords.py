import gensim
import pandas as pd
import csv
import re
import itertools
import pickle


from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora




p = open("/Users/Zelong/Desktop/桌面/研究生课程/Q1/2IMM15 Web information retrieval and data mining/nips-papers/papers.csv")
csvreader_papers = csv.reader(p)
papers_withhead = list(csvreader_papers)
papers_withouthead = papers_withhead[1:len(papers_withhead)]
'''
del papers_withouthead[5325]
del papers_withouthead[6497]
del papers_withouthead[6460]
del papers_withouthead[6424]
del papers_withouthead[5722]
del papers_withouthead[6013]

'''

a = open("/Users/Zelong/Desktop/桌面/研究生课程/Q1/2IMM15 Web information retrieval and data mining/nips-papers/authors.csv")
csvreader_author = csv.reader(a)
authors_withhead = list(csvreader_author)
authors_withouthead = authors_withhead[1:len(authors_withhead)]
#authors_withouthead = authors_withhead[1:300]


f = open("/Users/Zelong/Desktop/桌面/研究生课程/Q1/2IMM15 Web information retrieval and data mining/nips-papers/paper_authors.csv")
csvreader = csv.reader(f)
paper_authors_withhead = list(csvreader)
paper_authors_withouthead = paper_authors_withhead[1:len(paper_authors_withhead)]
#paper_authors_withouthead = paper_authors_withhead[1:300]




# pick up the useful key words from topic
def findoutkeywords(Topics, papers_id ): #  问题在这个function里

    firstlist=[]
    secondlist=[]
    thirdlist=[]
    fourthlist=[]
    a = papers_id

    for topic in Topics:
        keywords1 = topic[1].split("+")
        firstlist.append(keywords1)

    for l in firstlist:
        for m in l:
            keywords2 = m.split("*")
            secondlist.append(keywords2[1])

    for j in secondlist:
        third = re.findall(r'"([^"]*)"', j)  # pick up string between Double quotes
        thirdlist.extend(third)
        fourthlist = [a] + thirdlist # 在这里加上 author name 或者 authorID

    return fourthlist
    #return thirdlist



# generate topics and keywords from authors papers
def keywords_generatetopic(doc_a,paper_id):

    Texts = []
    tokenizer = RegexpTokenizer(r'\w+')
    b = paper_id

    #file = item.lower()
    file = doc_a.lower()   # only for test
    Tokens = tokenizer.tokenize(file)

    # Stop words--------
    # In this section, we will remove the useless word from the file/document
    stop_words_english = get_stop_words('english')  # create English stop words list

    #UPDATE THE STOP WORDS
    # stop_words_english is a list
    stop_words_english.extend(('0','1', '2', '3', '4', '5', '6', '7', '8', '9'))
    stop_words_english.extend(('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm'))

    # remove the stop words in tokens
    StoppedTokens = [i for i in Tokens if i not in stop_words_english]

    # Stemming-------
    # In the section, we will use stemming method to merge the words in which they have same meaning.
    # Create p_stemmer in class PorterStemmer
    p_stemmer = PorterStemmer()

    # Stem the stopped tokens
    StemmedTokens = [p_stemmer.stem(i) for i in StoppedTokens]
    Texts.append(StemmedTokens)  # put all stemmed stopped token words in a list


    # Constructing a document-term matrix-------
    dictionary = corpora.Dictionary(Texts)
    if dictionary == {}:
        result = [b]+['No Key words']
    else:
    # The doc2bow() function converts dictionary into a bag-of-words
        corpus = [dictionary.doc2bow(text) for text in Texts]  # until now runs good
    # Applying the LDA model----------
        LDA_Model = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=20)

        Topic = LDA_Model.print_topics(num_topics=2, num_words=5)
        # num_words means use number of words to describe the author
        result = findoutkeywords(Topic, paper_id)  # 这是一个methord

    return result


ID_Keywords_list = []

for item in papers_withouthead:
    keywords_list = keywords_generatetopic(item[6], item[0])
    ID_Keywords_list.append(keywords_list)

    print(ID_Keywords_list)



# store lists by pickle
with open('ID_KEYWORDS_new.pickle', 'wb') as handle:
    pickle.dump(ID_Keywords_list, handle, protocol=pickle.HIGHEST_PROTOCOL)