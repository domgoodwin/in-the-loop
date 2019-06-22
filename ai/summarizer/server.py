#!flask/bin/python
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
  print(input)
  json_string = json.dumps(input)
  print(json_string)
  return jsonify(summarize(input))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')