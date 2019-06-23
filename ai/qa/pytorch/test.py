from pytorch_pretrained_bert import modeling, BertConfig
from run_squad import *
import json

init_checkpoint_pt = "../files/models/squad/pytorch_model.bin"
bert_config = "../files/models/squad/bert_config.json"
device = torch.device("cpu")

bert_config_path = "../files/models/squad/config.json"
bert_config = BertConfig.from_json_file(bert_config_path)
model = modeling.BertForQuestionAnswering(bert_config)
#model = BertForQuestionAnswering.from_pretrained(init_checkpoint_pt)
model.load_state_dict(torch.load(init_checkpoint_pt, map_location='cpu'))
model.to(device)
model.qa_outputs.weight.data.fill_(1.0)
model.qa_outputs.bias.data.zero_()
all_input_ids = torch.tensor([f.input_ids for f in eval_features], dtype=torch.long)
all_input_mask = torch.tensor([f.input_mask for f in eval_features], dtype=torch.long)
all_segment_ids = torch.tensor([f.segment_ids for f in eval_features], dtype=torch.long)
all_example_index = torch.arange(all_input_ids.size(0), dtype=torch.long)
all_start_positions = torch.tensor([[f.start_position] for f in eval_features], dtype=torch.long)
all_end_positions = torch.tensor([[f.end_position] for f in eval_features], dtype=torch.long)

eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids,
                                   all_start_positions, all_end_positions, all_example_index)
eval_sampler = SequentialSampler(eval_data)
eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=1)

model.eval()
None
batch = iter(eval_dataloader).next()
input_ids, input_mask, segment_ids, start_positions, end_positions, example_index = batch
print([t.shape for t in batch])
start_positions.size()
pytorch_all_out = []
for batch in tqdm(eval_dataloader, desc="Evaluating"):
    input_ids, input_mask, segment_ids, start_positions, end_positions, example_index = batch
    input_ids = input_ids.to(device)
    input_mask = input_mask.to(device)
    segment_ids = segment_ids.to(device)
    start_positions = start_positions.to(device)
    end_positions = end_positions.to(device)

    total_loss, (start_logits, end_logits) = model(input_ids, segment_ids, input_mask, start_positions, end_positions)
    
    eval_feature = eval_features[example_index.item()]

    output_json = collections.OrderedDict()
    output_json["linex_index"] = unique_id
    output_json["tokens"] = [token for (i, token) in enumerate(eval_feature.tokens)]
    output_json["total_loss"] = total_loss.detach().cpu().numpy()
    output_json["start_logits"] = start_logits.detach().cpu().numpy()
    output_json["end_logits"] = end_logits.detach().cpu().numpy()
    pytorch_all_out.append(output_json)
    break
pytorch_outputs = [pytorch_all_out[0]['start_logits'], pytorch_all_out[0]['end_logits'], pytorch_all_out[0]['total_loss']]
