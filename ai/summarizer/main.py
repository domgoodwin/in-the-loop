import os
import json
import re
import shutil
import argparse
from argparse import Namespace
from prepro import data_builder
from train import test
import sentence_splitter
import nltk.data

def match_sentence(sentences, sentence_lw):
  out_summary = ''
  for sentence in sentences:
    if re.sub(r'\s','', sentence.lower()) == re.sub(r'\s','', sentence_lw.lower()):
      return sentence

def summarize(input, num_sen = 3):
  print(input)
  input = json.loads(input)
  articles = input.get("articles")

  bert_data_path = './files/my_bert_data/'
  log_file = './files/logs/output.log'
  model_path = './files/models/cnndm_bertsum_classifier_best.pt'
  results_path = './files/results/'
  json_path = './files/json'

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
  args.model_path = './files/models/'
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

  #init_logger(args.log_file)
  device = "cpu" if args.visible_gpus == '-1' else "cuda"
  device_id = 0 if device == "cuda" else -1

  cp = args.model_name
  #step = int(cp.split('.')[-2].split('_')[-1])
  step = 1000000

  test(args, device_id, cp, step)

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
      "wITH ITS mini-allotments, bicycle club and lively restaurant, the plan outlined by Tonic Living looks like the blueprint of any other retirement community. The difference is that most of the residents of Tonics proposed development would be lesbian, gay, bisexual or transgender. The organisation, founded in 2014, is hoping to find a site within a year for what would be Britains first retirement home for LGBT people. The thinking behind it is that for the million or so gay over-60s in Britain, the path towards assisted living can be especially tricky. They are likelier than other pensioners to live alone. Fewer than half have children. And almost three-quarters say they would worry about disclosing their sexuality to carers. Anna Kear, Tonics boss, says many old folk go back into the closet once they are dependent on care. Hers is not the only organisation planning homes for LGBT OAPs. Another group, London Older Lesbians Co-housing (LOLC), is also on the lookout for a site in the capital. Founded three years ago, it has about 35 women aged over 50 on its waiting list. It hopes to build a base and move in within five years. Both it and Tonic are supported by the Greater London Authority. The law allows groups with protected characteristics, including LGBT folk, to discriminate in their admissions (Tonic nonetheless accepts applications from all). The projects are partly inspired by organisations like the rainbow-adorned LebensortVielfalt in Berlin and Triangle Square in Los Angeles, which house elderly gay people. They also have a model in groups like Older Womens Co-Housing (OWCH), a development in London for women over 50 (straight and gay alike) which opened in 2016. The 26 residents wanted to preserve their independence in old age. We decided we would not be done unto, says Maria Brenton, the project manager. OWCH receives dozens of inquiries a week. Group living offers camaraderie as well as a spirit of radicalism that appeals to some activists. Were used to a combination of autonomy and collectivity as part of our lesbian feminism, says Liz Kelly, 67, who co-founded LOLC. Why would we want to conform to convention now, just because were older?. Social opportunities for older gay folk are improving in other ways, too. Opening Doors London organises walks, film nights and a befriending scheme for over-50s. Sally Knocker, who runs the charitys Rainbow Memory Caf, says people are finding innovative ways to combat isolation. As Ms Kear puts it, We have to get it across to them that its OK to be old and out and proud."
    ]
  }
  summaries = summarize(json.dumps(input))
  print(str(summaries))
