import re
from goose3 import Goose
from requests import get

def get_article_content(url):
  print("Getting article content for: ")
  print(url)
  response = get(url)
  extractor = Goose()
  article = extractor.extract(raw_html=response.content)
  title = article.title
  text = article.cleaned_text
  # Remove non-ascii characters
  text = re.sub(r'[^\x00-\x7F]+',' ', text)
  text = re.sub(r'\n',' ', text)
  text = re.sub(r'\'','', text)
  text = re.sub(r'\"','', text)
  return title, text

if __name__ == '__main__':
  print(get_article_content('https://www.dailymail.co.uk/news/article-7170867/Carrie-Symonds-scared-home-recorded-political-stich-neighbours.html'))