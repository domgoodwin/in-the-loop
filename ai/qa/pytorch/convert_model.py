from pytorch_pretrained_bert import BertForQuestionAnswering

model = BertForQuestionAnswering.from_pretrained(
  '../files/models/uncased_L-24_H-1024_A-16/',
  cache_dir=None,
  from_tf=True,
  state_dict=None
  #*input,
  #**kwargs
)