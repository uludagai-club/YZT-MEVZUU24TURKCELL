from transformers import BertTokenizer
from data_processing import load_data, process_data, prepare_datasets
from model_training import train_model
from aspects_extracting import extract_aspects_and_sentiments

file_path = 'turkcell_.json'
data = load_data(file_path)

tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-base-turkish-uncased")
input_ids, attention_masks, label_ids, label_list = process_data(data, tokenizer)

train_dataset, val_dataset = prepare_datasets(input_ids, attention_masks, label_ids)

model = train_model(train_dataset, val_dataset, tokenizer, label_list)

text = "Turkcell Superbox hizmeti berbat."
aspects = extract_aspects_and_sentiments(text, model, tokenizer, label_list)
print(aspects)
