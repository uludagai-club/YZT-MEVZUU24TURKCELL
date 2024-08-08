import sys
import os
"""current_dir = os.path.dirname(os.path.join(os.path.dirname(__file__)))
parent_dir = os.path.dirname(current_dir)
up_parent_dir = os.path.dirname(parent_dir)
up2_parent_dir = os.path.dirname(up_parent_dir)
sys.path.append(parent_dir)
sys.path.append(up_parent_dir)
sys.path.append(up2_parent_dir)"""
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from tools import prepare_data 

def train_model(df):
    model_name = "dbmdz/bert-base-turkish-cased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name, num_labels=3)
    
    inputs, labels = prepare_data(df, tokenizer)
    
    class SentimentDataset(torch.utils.data.Dataset):
        def __init__(self, inputs, labels):
            self.inputs = inputs
            self.labels = labels
        
        def __len__(self):
            return len(self.labels)
        
        def __getitem__(self, idx):
            return {key: val[idx] for key, val in self.inputs.items()}, self.labels[idx]

    dataset = SentimentDataset(inputs, labels)

    logging_dir = "/logs"  # Mevcut dizinde 'logs' dizini
    output_dir = "/results"  # Mevcut dizinde 'results' dizini

    # Dizinlerin mevcut olup olmadığını kontrol et ve gerekiyorsa oluştur
    os.makedirs(logging_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        label_names=['text'],
        logging_dir=logging_dir,
    )

    os.makedirs(logging_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        eval_dataset=dataset,
    )

    trainer.train()
    return model, tokenizer

def evaluate_model(model, tokenizer, df):
    inputs, labels = prepare_data(df, tokenizer)
    dataset = train_model.SentimentDataset(inputs, labels)
    
    trainer = Trainer(model=model)
    return trainer.evaluate(eval_dataset=dataset)