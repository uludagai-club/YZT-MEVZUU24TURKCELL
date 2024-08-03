import json
import torch
from torch.utils.data import DataLoader, TensorDataset
from transformers import BertTokenizer

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def tokenize_and_preserve_labels(sentence, annotations, tokenizer):
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

def encode_labels(labels, label_map, max_length=128):
    encoded_labels = [label_map[label] for label in labels]
    encoded_labels = encoded_labels[:max_length]
    encoded_labels += [0] * (max_length - len(encoded_labels))
    return encoded_labels

def process_data(data, tokenizer, max_length=128):
    texts = [entry['data']['text'] for entry in data]
    annotations = [[{
                        'text': result['value']['text'],
                        'start': result['value']['start'],
                        'end': result['value']['end'],
                        'label': result['value']['labels'][0]
                    } for annotation in entry['annotations'] for result in annotation['result']] for entry in data]

    tokenized_texts_and_labels = [
        tokenize_and_preserve_labels(text, annotation, tokenizer)
        for text, annotation in zip(texts, annotations)
    ]

    label_list = list(set([ann['label'] for sublist in annotations for ann in sublist] + ['O']))
    label_map = {label: i for i, label in enumerate(label_list)}

    input_ids = []
    attention_masks = []
    label_ids = []

    for tokenized_sentence, labels in tokenized_texts_and_labels:
        encoded_dict = tokenizer.encode_plus(
            tokenized_sentence,
            add_special_tokens=True,
            max_length=max_length,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
            truncation=True
        )

        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])
        label_ids.append(torch.tensor(encode_labels(labels, label_map, max_length=max_length), dtype=torch.long))

    return torch.stack(input_ids).squeeze(1), torch.stack(attention_masks).squeeze(1), torch.stack(label_ids), label_list

def prepare_datasets(input_ids, attention_masks, label_ids, train_size=0.8):
    dataset = TensorDataset(input_ids, attention_masks, label_ids)
    train_size = int(train_size * len(dataset))
    val_size = len(dataset) - train_size
    return torch.utils.data.random_split(dataset, [train_size, val_size])
