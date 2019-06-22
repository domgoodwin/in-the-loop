import os
import re
import json
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


  model_dir = '../files/models/uncased_L-24_H-1024_A-16/'
  model_name = 'out_model.ckpt-10859' # this does not include .data...
  predict_file = '../files/json/my-data.json'
  
  qa_json = create_qa_json(input)
  with open(predict_file, 'w+') as f:
    f.write(json.dumps(qa_json))

  run_command = """python run_squad.py
  --vocab_file={}
  --bert_config_file={}
  --init_checkpoint={}
  --predict_batch_size=8
  --do_train=False
  --train_file="./files/train/train-v2.0.json"
  --do_predict=True
  --train_batch_size=24
  --learning_rate=3e-5
  --num_train_epochs=2.0
  --max_seq_length=384
  --doc_stride=128
  --output_dir={}
  --use_tpu=False
  --version_2_with_negative=True
  --null_score_diff_threshold=-4.032604694366455
  --predict_file={}
  """

  vocab_file = os.path.join(model_dir,"vocab.txt")
  bert_config_file = os.path.join(model_dir, "bert_config.json")
  init_checkpoint = os.path.join(model_dir, model_name)
  output_dir = "../files/results"
  predict_file = '../files/json/my-data.json'

  run_command = run_command.format(
    vocab_file,
    bert_config_file,
    init_checkpoint,
    output_dir,
    predict_file
  ).replace('\n', ' ')

  print(run_command)
  #os.system(run_command)
  subprocess.call(run_command.split(' '))

  with open('../files/results/predictions.json', 'r') as f:
    output = f.read()
  return output


if __name__ == '__main__':
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
  input = json.dumps(input)
  answers = answer_questions(input)
  print(answers)