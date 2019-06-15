import string
import nltk.data
from nltk.tokenize import word_tokenize
import __future__

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
fp = open("test.txt")
data = fp.read()
printable = set(string.printable)
data = filter(lambda x: x in printable, data)
sentences = tokenizer.tokenize(data)
for sentence in sentences:
    print(word_tokenize(sentence))
    print("\n")
