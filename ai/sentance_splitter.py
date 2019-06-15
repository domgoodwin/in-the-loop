import string
from nltk.tokenize import word_tokenize, sent_tokenize
import __future__

articles = []

def get_articles_json(articles):
    articles_json = []
    printable = set(string.printable)
    for article in articles:
        # Convert to lower and remove non-ascii chars
        article_cont = filter(lambda x: x in printable, str(article)).lower()
        # Split the sentences
        sentences = sent_tokenize(article_cont)
        # Split the sentences to words
        src = []
        for sentence in sentences:
            s_list = word_tokenize(sentence)
            src.append(s_list)
        article_json = {
            "src" : src,
            "tgt" : []
        }
        articles_json.append(article_json)
    return articles_json

articles = []
fp = open("test.txt")
data = fp.read()
articles.append(data)
print(str(get_articles_json(articles)))
        
