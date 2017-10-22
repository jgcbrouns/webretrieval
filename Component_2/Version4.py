import pickle


# ------------------------------------------------------
# reload stored data
with open('AuthorID_KEYWORDS_v3.pickle', 'rb') as handle:
    authors_id_keywords_dictionary = pickle.load(handle)


print(authors_id_keywords_dictionary)


# open a new outside data
co_author = pickle.load(open("/Users/Zelong/Desktop/桌面/研究生课程/Q1/2IMM15 Web information retrieval and data mining/nips-papers/pagerank_author_whole.dat", "rb"))


f_list=[]
for key, value in authors_id_keywords_dictionary.items():
    for k, v in co_author.items():
        if int(k) == int(key):
            s_list = [int(key)] + [v] + value
            f_list.append(s_list)





# store lists by pickle
with open('AuthorID_Value_KEYWORDS.pickle', 'wb') as handle:
    pickle.dump(f_list, handle, protocol=pickle.HIGHEST_PROTOCOL)


'''
author_ids = []
final_id = []
rank_value = []
li_new = []


for key, value in finaldict.items():
    #finaldict[key] = list(set(value))
    final_list = [key] + list(set(value))
    complex_list.append(final_list)


for au_id in co_author.keys():
    li_new.append(au_id)

for ite in li_new:
    for i in final_id:
        if str(ite) == i:  # 有时候无法匹配，得到空list 是因为这行的 两个对比数据的type 不一样
            if ite not in rank_value:
                rank_value.append(co_author[ite])
'''