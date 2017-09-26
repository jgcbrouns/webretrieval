import sqlite3, re, operator, math
from nltk.corpus import stopwords

# ---- some extra ideas for parsing: ----
# - remove one character words

class Data():

    @staticmethod
    def retrieve_data(input_file, n):
        conn = sqlite3.connect(input_file)
        c = conn.cursor()
        query = 'SELECT a.name author, COUNT(DISTINCT p.Id) num_papers FROM authors a INNER JOIN paper_authors pa ON a.id=pa.author_id INNER JOIN papers p ON pa.paper_id=p.id WHERE year=2016 GROUP BY a.name ORDER BY COUNT(DISTINCT p.Id) DESC LIMIT 100'
        query = 'SELECT * FROM papers ORDER BY id DESC LIMIT ' + str(n)
        query = c.execute(query)
        return query

    @staticmethod
    def prepare(text):
        stop = set(stopwords.words('english'))
        text = re.sub(r'[^\w]', ' ', text)
        return [i for i in text.lower().split() if i not in stop]

    @staticmethod
    def calculate(keywords):
        count = {}
        for key in keywords:
            if key in count:
                count[key] += 1
            else:
                count[key] = 1
        return count

    @staticmethod
    def sort(array, desc = True):
        return sorted(array.items(), key=operator.itemgetter(1), reverse=desc)

    @staticmethod
    def concat_counts(counts):
        df = {}
        for count in counts.values():
            for key in count:
                if key in df:
                    df[key] += count[key]
                else:
                    df[key] = count[key]
        return df

    @staticmethod
    def idf(df, key, N):
        if key in df:
            return 1 + math.log10(N/df[key])
        return 1 + math.log10(N)

if __name__ == "__main__":
    texts = Data.retrieve_data('../data/database.sqlite', 100)
    tf = {}
    for text in texts:
        tokens = Data.prepare(text[6])
        count  = Data.calculate(tokens)
        tf[text[0]] = count
    df = Data.concat_counts(tf)
    # sort_df = Data.sort(df, False)
    print(df)
