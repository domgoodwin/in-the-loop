import os
import re
import json
import wikipedia
import subprocess
import run_squad
from argparse import Namespace

def create_qa_json(input):
  input = json.loads(input)
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

def answer_questions(input):


  model_dir = '../files/models/cased_L-12_H-768_A-12/' #uncased_L-24_H-1024_A-16/'
  model_name = 'out_model.ckpt-10859' # this does not include .data...
  predict_file = '../files/json/my-data.json'
  
  qa_json = create_qa_json(input)
  with open(predict_file, 'w+') as f:
    f.write(json.dumps(qa_json))

  bert_model = "../files/models/squad/"
  output_dir = "../files/results"
  predict_file = '../files/json/my-data.json'

  args = Namespace()
  args.bert_model = bert_model
  args.predict_batch_size=16
  args.do_predict=True
  args.max_seq_length=384
  args.doc_stride=128
  args.output_dir=output_dir
  args.version_2_with_negative = False
  args.null_score_diff_threshold=-4.005961775779724
  args.predict_file=predict_file
  args.overwrite_output_dir=True
  args.do_lower_case=True

  args.train_file = None
  args.max_query_length=64
  args.do_train=False
  args.train_batch_size=32
  args.learning_rate=5e-5
  args.num_train_epochs=3.0
  args.warmup_proportion=0.1
  args.n_best_size=20
  args.max_answer_length=30
  args.verbose_logging=False
  args.no_cuda=False
  args.seed=42
  args.gradient_accumulation_steps=1
  args.local_rank=-1
  args.fp16=False
  args.loss_scale=0
  args.version_2_with_negative=False
  args.null_score_diff_threshold=0.0
  args.server_ip=''
  args.server_port=''

  run_squad.main(args)

  with open('../files/results/predictions.json', 'r') as f:
    output = f.read()
  return json.loads(output)


if __name__ == '__main__':
  page = wikipedia.page('History of the United Kingdom')

  input = {
    "data" : [
      {
        "questions" : [
          "When was the welfare state expanded?",
          "Who won the election in 1997?",
          "What was the result of the Scottish referendum?"
        ],
        "context" : str(page.content)
      }
    ]
  }
  input = json.dumps(input)
  answers = answer_questions(input)
  print(answers)

