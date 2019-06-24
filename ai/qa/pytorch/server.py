#!flask/bin/python
from flask import Flask, request, jsonify
from main import answer_questions
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/qa', methods=['POST'])
def get_summary():
  input = request.data.decode('utf-8')
  json_string = json.dumps(input)
  output = answer_questions(input)
  print(input)
  print(type(input))
  print(output)
  print(type(output))
  for d in json.loads(input)["data"]:
    count = 0
    for q in d["questions"]:
      output[q] = output.pop(str(count))
      count += 1

  return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')