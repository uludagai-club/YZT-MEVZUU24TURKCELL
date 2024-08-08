import torch

def prepare_data(df, tokenizer, max_length=128):
    texts = df["text"].tolist()
    labels = [[1 if s == "olumlu" else 0 if s == "nötr" else 2 for s in sentiment] for sentiment in df["sentiments"]]
    max_label_length = max(len(label) for label in labels)
    padded_labels = [label + [0] * (max_label_length - len(label)) for label in labels]
    
    inputs = tokenizer(texts, max_length=max_length, padding=True, truncation=True, return_tensors="pt")
    labels = torch.tensor(padded_labels)
    return inputs, labels

def predict_sentiment(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    
    # Modelin 2D çıktısını ele almak için argmax işlemini dim=1 üzerinde yapıyoruz
    predictions = torch.argmax(outputs.logits, dim=1).tolist()
    
    return predictions

def generate_output(df, model, tokenizer):
    output = []
    for index, row in df.iterrows():
        text = row["text"]
        entities = row["entities"]
        predictions = predict_sentiment(text, model, tokenizer)
        entity_sentiment = [{"entity": entity, "sentiment": "olumlu" if pred == 1 else "olumsuz" if pred == 2 else "nötr"} for entity, pred in zip(entities, predictions)]
        output.append({
            "entity_list": entities,
            "results": entity_sentiment
        })
    return output

def extract_entities(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=1).tolist()  # 2D çıktıyı ele alıyoruz

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    entities = []
    current_entity = []

    for token, prediction in zip(tokens, predictions):
        label = model.config.id2label[prediction]
        if label.startswith("B-"):
            if current_entity:
                entities.append(" ".join(current_entity))
                current_entity = []
            current_entity.append(token)
        elif label.startswith("I-") and current_entity:
            current_entity.append(token)
        else:
            if current_entity:
                entities.append(" ".join(current_entity))
                current_entity = []
    
    if current_entity:
        entities.append(" ".join(current_entity))
    
    entities = [entity.replace("##", "") for entity in entities]
    
    return entities

def generate_output_textbase(text, model, tokenizer):
    output = []
    
    entities = extract_entities(text, tokenizer, model)
    
    predictions = predict_sentiment(text, model, tokenizer)
    
    entity_sentiment = [{"entity": entity, "sentiment": "olumlu" if pred == 1 else "olumsuz" if pred == 2 else "nötr"} for entity, pred in zip(entities, predictions)]
    
    output.append({
        "entity_list": entities,
        "results": entity_sentiment
    })
    
    return output

def calculate_score(predicted_output, ground_truth):
    correct_entity_count = sum([1 for po, gt in zip(predicted_output["results"], ground_truth["results"]) if po["entity"] == gt["entity"]])
    correct_sentiment_count = sum([1 for po, gt in zip(predicted_output["results"], ground_truth["results"]) if po["sentiment"] == gt["sentiment"]])

    entity_score = correct_entity_count / max(len(predicted_output["results"]), len(ground_truth["results"]))
    sentiment_score = correct_sentiment_count / max(len(predicted_output["results"]), len(ground_truth["results"]))
    
    overall_score = 0.65 * entity_score + 0.35 * sentiment_score
    return overall_score