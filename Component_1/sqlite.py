import sqlite3
conn = sqlite3.connect('../data/database.sqlite')
c = conn.cursor()
query = 'SELECT a.name author, COUNT(DISTINCT p.Id) num_papers FROM authors a INNER JOIN paper_authors pa ON a.id=pa.author_id INNER JOIN papers p ON pa.paper_id=p.id WHERE year=2016 GROUP BY a.name ORDER BY COUNT(DISTINCT p.Id) DESC LIMIT 100'
query = 'SELECT * FROM papers ORDER BY id DESC LIMIT 1'
query = c.execute(query)
for row in query:
    print(row[5])

from nltk import word_tokenize
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
sentence = row[5]
print([i for i in sentence.lower().split() if i not in stop])