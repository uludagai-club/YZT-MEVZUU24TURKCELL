import torch
from transformers import BertForTokenClassification, Trainer, TrainingArguments, DataCollatorForTokenClassification

def train_model(train_dataset, val_dataset, tokenizer, label_list, output_dir='./results', logging_dir='./logs'):
    model = BertForTokenClassification.from_pretrained("dbmdz/bert-base-turkish-uncased", num_labels=len(label_list))

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=logging_dir,
        logging_steps=10,
    )

    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

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
    return model