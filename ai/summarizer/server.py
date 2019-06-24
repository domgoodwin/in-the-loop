#!flask/bin/python
from article_scrape import get_article_content
from flask import Flask, request, jsonify
from main import summarize
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/summary', methods=['POST'])
def get_summary():
  input = request.data.decode('utf-8')
  input_json = json.loads(input)

  articles = []
  details = []
  for article in input_json.get("articles"):
    if 'url' in article:
      url = article.get('url')
      article_title, article_text = get_article_content(url)
    else:
      article_text = article
      article_title = ""
      url = ""
    details_json = {
      "title" : article_title,
      "text" : article_text,
      "link" : url
    }
    details.append(details_json)
    articles.append(article_text)
  articles_json = { "articles" : articles }
  summaries = summarize(json.dumps(articles_json)).get("output")
  print(summaries)
  details[0]["summary"] = []
  for summary in summaries:  
    details[0]["summary"].append(summary)
  
  output = { "output" : details}
  print(output)
  return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')