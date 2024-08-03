import torch

def extract_aspects_and_sentiments(text, model, tokenizer, label_list):
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
