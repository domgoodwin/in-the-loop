from fast_bert.prediction import BertClassificationPredictor

MODEL_PATH = '../files/models/uncased_L-24_H-1024_A-16'
BERT_PRETRAINED_PATH = '../files/models/uncased_L-24_H-1024_A-16'
LABEL_PATH = '../files/results/'

predictor = BertClassificationPredictor(model_path=MODEL_PATH, pretrained_path=BERT_PRETRAINED_PATH, 
                                        label_path=LABEL_PATH, multi_label=False)

# Single prediction
single_prediction = predictor.predict("just get me result for this text")

# Batch predictions
texts = [
  "this is the first text",
  "this is the second text"
]

multiple_predictions = predictor.predict(texts)