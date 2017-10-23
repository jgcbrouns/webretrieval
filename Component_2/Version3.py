import pickle
import csv

a = open("/Users/Zelong/Desktop/桌面/研究生课程/Q1/2IMM15 Web information retrieval and data mining/nips-papers/authors.csv")
csvreader_author = csv.reader(a)
authors_withhead = list(csvreader_author)
authors_withouthead = authors_withhead[1:len(authors_withhead)]


# ------------------------------------------------------
# reload stored data
with open('AuthorID_KEYWORDS.pickle', 'rb') as handle:
    authors_id_keywords_dictionary = pickle.load(handle)


#print(authors_id_keywords_dictionary)


# open a new outside data
co_author = pickle.load(open("/Users/Zelong/Desktop/桌面/研究生课程/Q1/2IMM15 Web information retrieval and data mining/nips-papers/pagerank_author_whole.dat", "rb"))

print(co_author.items())



# search author name by keywords
def search_for_author(keywords_list):

    author_ids = []
    final_id=[]
    rank_value=[]
    li_new=[]

    '''
    # check for one key words
    for item in authors_id_keywords_dictionary[0:1000]:
        for s in item[1:]:
            if str(s) == str(keywords):
                if item not in author_ids:
                    author_ids.append(item[0])
                else:
                    author_ids = [0]
    '''
    # check for multiple key words together
    for item in authors_id_keywords_dictionary:
        if all(word in item[1:] for word in keywords_list):
            author_ids.append(item[0])


    for x in author_ids:
        if x not in final_id:
            final_id.append(x)
    print("This is the final author id lists from keywords search------->{}".format(final_id))




    for au_id in co_author.keys():
        li_new.append(au_id)

    for ite in li_new:
        for i in final_id:
            if str(ite) == i: # 有时候无法匹配，得到空list 是因为这行的 两个对比数据的type 不一样
                if ite not in rank_value:
                    rank_value.append(co_author[ite])


    #print("This is the rank value of  author id lists------->{}".format(rank_value))

    result1 = seach_for_authorname(final_id)  # This is a method

    result = dict(zip(result1[0:5], rank_value[0:5]))

    return result


# 通过ID 寻找author name
def seach_for_authorname(ids):
    author_names = []
    for a_id in authors_withouthead:
        for b_id in ids:
            if a_id[0] == b_id:
                author_names.append(a_id[1])

    return author_names


# search author name by Key words!!!!!!!!
key_word1 = 'network'
key_word2 = 'control'
key_word3 = 'neural'
key_word_list = [key_word1]+[key_word2]+[key_word3]


AUTHOR_NAME = search_for_author(key_word_list)

print("The authors name are {}".format(AUTHOR_NAME))

# Rank author name

S = [(k, AUTHOR_NAME[k]) for k in sorted(AUTHOR_NAME, key=AUTHOR_NAME.get, reverse=True)]

print("The rank result of authors are in the below:")
for k, v in S:
    print("%s: %s" % (k, v))

