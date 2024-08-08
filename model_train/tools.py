import torch


def prepare_data(df, tokenizer, max_length=128):
    texts = df["text"].tolist()
    labels = [[1 if s == "olumlu" else 0 if s == "nötr" else 2 for s in sentiment] for sentiment in df["sentiments"]]
    max_label_length = max(len(label) for label in labels)
    padded_labels = [label + [0] * (max_label_length - len(label)) for label in labels]  # Pad with a neutral label or other value if appropriate
    
    inputs = tokenizer(texts, max_length=max_length, padding=True, truncation=True, return_tensors="pt")
    labels = torch.tensor(padded_labels)
    return inputs, labels

def predict_sentiment(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
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

def generate_output_textbase(text, entities, model, tokenizer):
    output = []

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