import json
from transformers import BertTokenizer
import torch
from torch.utils.data import DataLoader, TensorDataset
from transformers import BertForTokenClassification, Trainer, TrainingArguments, DataCollatorForTokenClassification


with open('turkcell_.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-base-turkish-uncased")

texts = []
annotations = []

for entry in data:
    texts.append(entry['data']['text'])
    anns = []
    for annotation in entry['annotations']:
        for result in annotation['result']:
            anns.append({
                'text': result['value']['text'],
                'start': result['value']['start'],
                'end': result['value']['end'],
                'label': result['value']['labels'][0]
            })
    annotations.append(anns)

# print(texts[0])
# print(annotations[0])

def tokenize_and_preserve_labels(sentence, annotations):
    tokenized_sentence = []
    labels = []

    for word in sentence.split():
        tokenized_word = tokenizer.tokenize(word)
        n_subwords = len(tokenized_word)

        label = "O"
        for ann in annotations:
            if ann['text'] in word:
                label = ann['label']

        tokenized_sentence.extend(tokenized_word)
        labels.extend([label] * n_subwords)

    return tokenized_sentence, labels

tokenized_texts_and_labels = [
    tokenize_and_preserve_labels(text, annotation)
    for text, annotation in zip(texts, annotations)
]

# print(tokenized_texts_and_labels[0])

label_list = list(set([ann['label'] for sublist in annotations for ann in sublist] + ['O']))
label_map = {label: i for i, label in enumerate(label_list)}

def encode_labels(labels, max_length=128):
    encoded_labels = [label_map[label] for label in labels]
    encoded_labels = encoded_labels[:max_length]
    encoded_labels += [0] * (max_length - len(encoded_labels))
    return encoded_labels

input_ids = []
attention_masks = []
label_ids = []

for tokenized_sentence, labels in tokenized_texts_and_labels:
    encoded_dict = tokenizer.encode_plus(
        tokenized_sentence,
        add_special_tokens=True,
        max_length=128,
        padding='max_length',
        return_attention_mask=True,
        return_tensors='pt',
        truncation=True
    )

    input_ids.append(encoded_dict['input_ids'])
    attention_masks.append(encoded_dict['attention_mask'])
    label_ids.append(torch.tensor(encode_labels(labels, max_length=128), dtype=torch.long))

label_ids = torch.stack(label_ids)

input_ids = torch.stack(input_ids)
attention_masks = torch.stack(attention_masks)

dataset = TensorDataset(
    input_ids.squeeze(1),
    attention_masks.squeeze(1),
    label_ids
)

train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

model = BertForTokenClassification.from_pretrained("dbmdz/bert-base-turkish-uncased", num_labels=len(label_list))

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
)

def custom_data_collator(features):
    features = [{'input_ids': feature[0], 'attention_mask': feature[1], 'labels': feature[2]} for feature in features]
    return data_collator(features)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    data_collator=custom_data_collator
)
trainer.train()

# Deneme
def extract_aspects_and_sentiments(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    outputs = model(**inputs).logits
    predictions = torch.argmax(outputs, dim=2)

    tokens = tokenizer.convert_ids_to_tokens(inputs.input_ids[0])
    predicted_labels = [label_list[pred] for pred in predictions[0]]

    aspects = []
    for token, label in zip(tokens, predicted_labels):
        if label != "O":
            aspects.append((token, label))

    return aspects

text = "Turkcell Superbox hizmeti berbat."
aspects = extract_aspects_and_sentiments(text, model, tokenizer)
print(aspects)