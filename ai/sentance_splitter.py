import string
import nltk.data
from nltk.tokenize import word_tokenize
import __future__

articles = []

def get_articles_json(articles):
    articles_json = []
    printable = set(string.printable)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    for article in articles:
        # Convert to lower and remove non-ascii chars
        article_cont = filter(lambda x: x in printable, str(article)).lower()
        # Use the nltk sentence splitter to get the sentences
        sentences = tokenizer.tokenize(article_cont)
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
        
