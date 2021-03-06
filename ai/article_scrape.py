import re
from goose3 import Goose
from requests import get

def get_article_content(url):
  print("Loading in article"+url)
  response = get(url)
  extractor = Goose()
  article = extractor.extract(raw_html=response.content)
  text = article.cleaned_text
  # Remove non-ascii characters
  text = re.sub(r'[^\x00-\x7F]+',' ', text)
  return text

print(get_article_content('https://www.dailymail.co.uk/news/article-7170867/Carrie-Symonds-scared-home-recorded-political-stich-neighbours.html'))