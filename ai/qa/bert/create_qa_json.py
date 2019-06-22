import re
import json

def create_qa_json(input):

  question_id = 0
  title_id = 0
  formatted_data = []
  for qa_pair in input.get('data'):
    questions = qa_pair.get('questions')
    context = qa_pair.get('context')
    # Remove non-ascii chars and newlines from context
    context = re.sub(r'[^\x00-\x7F]+',' ', context).replace('\n', " ")
    qas = []
    for question in questions:
      question_json = {
        "question" : question,
        "id" : str(question_id),
        "answers" : [],
        "is_impossible": False
      }
      qas.append(question_json)
      question_id += 1
      qa_json = {
        "title" : "Test" + str(title_id),
        "paragraphs" : [
          {
            "qas" : qas,
            "context" : context
          }
        ]
      }
      formatted_data.append(qa_json)
      title_id += 1

  json_data = {
    "version": "v2.0",
    "data": formatted_data
  }
  return json_data
  

input = {
  "data" : [
    {
      "questions" : [
        "What is love?",
        "What is the answer?"
      ],
      "context" : "Love is the answer and the answer is love!"
    },
    {
      "questions" : [
        "What's time?"
      ],
      "context" : "Time is what's measured by a clock"
    },
  ]
}

create_qa_json(input)