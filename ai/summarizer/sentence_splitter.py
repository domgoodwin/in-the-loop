import re
from nltk.tokenize import word_tokenize, sent_tokenize

articles = []

def get_articles_json(articles):
    articles_json = []
    all_sentences = []
    for article in articles:
        # Remove non-ascii chars
        article_cont = re.sub(r'[^\x00-\x7F]+',' ', article)
        article_cont = re.sub('(?=[^\.])\n\s*(?=\S)', r'. ', article_cont, flags = re.M)
        article_cont = re.sub('([^\.])\.\. ', r'\1. ', article_cont, flags = re.M)
        # Split the sentences
        sentences = sent_tokenize(article_cont)
        # Split the sentences to words
        src = []
        for sentence in sentences:
            # Need to make sentences lower case
            s_list = word_tokenize(sentence.lower())
            src.append(s_list)
        article_json = {
            "src" : src,
            "tgt" : []
        }
        articles_json.append(article_json)
        all_sentences.append(sentences)
    return articles_json, all_sentences