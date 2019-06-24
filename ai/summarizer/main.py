import os
import json
import re
import shutil
import argparse
from argparse import Namespace
from prepro import data_builder
import train
import sentence_splitter
import nltk.data


def summarize(input, num_sen = 3):
  print(input)
  input = json.loads(input)
  articles = input.get("articles")

  bert_data_path = './files/my_bert_data/'
  log_file = './files/logs/output.log'
  model_path = './files/models/cnndm_bertsum_classifier_best.pt'
  results_path = './files/results/'
  json_path = './files/json/'

  bert_data, all_sentences = sentence_splitter.get_articles_json(articles)

  with open(os.path.join(json_path,"test.1.json"), 'w+') as f:
      f.write(json.dumps(bert_data))

# Format to Bert
  args = Namespace()
  args.dataset = 'test'
  args.raw_path = json_path
  args.save_path = './files/bert.pt/'
  args.log_file = log_file
  args.oracle_mode = 'greedy'
  args.map_path = './files/data/'
  args.shard_size = 2000
  args.min_nsents = 3
  args.max_nsents = 100
  args.min_src_ntokens = 5
  args.max_src_ntokens = 200
  args.lower = True
  args.n_cpus = 2

  data_builder.format_to_bert(args)
  # Rename the file
  shutil.move("./files/bert.pt/test.1.bert.pt", "./files/bert.pt/.test.pt")

  # Get the predictions
  args = Namespace()
  args.encoder = 'classifier'
  args.mode = 'test'
  args.bert_data_path = './files/bert.pt/'
  args.model_path = './models/'
  args.result_path = results_path
  args.temp_dir = './temp'
  args.batch_size = 1000
  args.use_interval = True
  args.large = False
  args.hidden_size = 128
  args.ff_size = 512
  args.heads = 4
  args.inter_layers = 2
  args.rnn_size = 512
  args.param_init = 0
  args.param_init_glorot = True
  args.dropout = 0.1
  args.optim = 'adam'
  args.lr = 1
  args.beta1 =  0.9
  args.beta2 = 0.999
  args.decay_method = ''
  args.warmup_steps = 8000
  args.max_grad_norm = 0
  args.save_checkpoint_steps = 5
  args.accum_count = 1
  args.world_size = 1
  args.report_every = 1
  args.train_steps = 1000
  args.recall_eval = False
  args.visible_gpus = '-1'
  args.gpu_ranks = '0'
  args.log_file = log_file
  args.dataset = ''
  args.seed = 358
  args.test_all = False
  args.model_name = model_path
  args.train_from = ''
  args.report_rouge = True
  args.block_trigram = True
  args.num_sen = num_sen
  args.gpu_ranks = [int(i) for i in args.gpu_ranks.split(',')]
  os.environ["CUDA_VISIBLE_DEVICES"] = args.visible_gpus

  train.test(args)
  def match_sentence(sentences, sentence_lw):
    out_summary = ''
    for sentence in sentences:
      if re.sub(r'\s','', sentence.lower()) == re.sub(r'\s','', sentence_lw.lower()):
        return sentence

  # Format the output (at this stage all summaries are in lower case - lw)
  with open(os.path.join(results_path,"_step1000000.candidate"), 'r') as f:
    summaries = f.read()
  output = []
  count = 0
  for summary_lw in summaries.splitlines():
    sentences = all_sentences[count]
    summary = ''
    for sentence_lw in summary_lw.split('<q>'):
      sentence = match_sentence(sentences, sentence_lw)
      output.append(sentence.strip())
    count += 1
  return { "output" : output }

if __name__ == '__main__':
  input = {
    "articles" : [
      "Oh hai Claudette! What's new with you? Anyway, how's your sex life? I'd do anything for my girl!",
      "I did naat heet her! It's bullshit, I did naat heet her, I did naaat!!! Oh, hai Mark? What's new with you?"
    ]
  }
  summaries = summarize(json.dumps(input))
  print(str(summaries))
