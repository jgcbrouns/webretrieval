
# coding: utf-8

# In[2]:

import pandas as pd
import numpy as np
co_author=np.zeros((9342,9342))#author number 9341
marks = pd.read_csv("F:/dataminin/nips-papers/paper_authors.csv")
for i in range(0,len(marks["id"])-8): #assume largest co author number is 8, literate firstly to length-8
    for j in range(i+1,i+8):
      if marks.iloc[i]["paper_id"]==marks.iloc[j]["paper_id"]:
        co_author[marks.iloc[i]["author_id"]][marks.iloc[j]["author_id"]]+=1
        co_author[marks.iloc[j]["author_id"]][marks.iloc[i]["author_id"]]+=1
for m in range(len(marks["id"])-8,len(marks["id"])-4):#look in to the rest
    for c in range(m+1,m+4):
        if marks.iloc[c]["paper_id"]==marks.iloc[m]["paper_id"]:
          co_author[marks.iloc[m]["author_id"]][marks.iloc[c]["author_id"]]+=1
          co_author[marks.iloc[c]["author_id"]][marks.iloc[m]["author_id"]]+=1
for a in range(len(marks["id"])-4,len(marks["id"])-1):
    if marks.iloc[a]["paper_id"]==marks.iloc[a+1]["paper_id"]:
        co_author[marks.iloc[a]["author_id"]][marks.iloc[a+1]["author_id"]]+=1
        co_author[marks.iloc[a+1]["author_id"]][marks.iloc[a]["author_id"]]+=1
for b in range(9342):
    for c in range(9342):
      if(b!=c and co_author[b][c]!=0):
        if(co_author[b][c]!=1):
            co_author[b][c]=1/co_author[b][c]*(co_author[b][c]-1)
        else:
            co_author[b][c]=0.18 # self defined， once cooperation should not be highly valued
co_author_sample1=np.zeros((500,500))
for row in range(500):
    for col in range(500):
        co_author_sample1[row][col]=co_author[row][col]
data1=pd.DataFrame(co_author_sample1)
data1.to_csv("F:/dataminin/nips-papers/co_authors_sample1.csv")
  



# In[3]:

import pandas as pd
import numpy as np
#co_author=np.ones((9341,9341))
marks = pd.read_csv("F:/dataminin/nips-papers/paper_authors.csv")
co_author=np.ones((9342,9342))
co_author
    

