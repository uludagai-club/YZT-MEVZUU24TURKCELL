import json

file_path = 'C:/Users/AYÇANUR/Downloads/turkcell.json'

with open(file_path, 'r', encoding='utf-8') as f:
    input_data = json.load(f)

output_data = {
    "text": [],
    "entities": [],
    "sentiments": []
}

for item in input_data: 
    if 'data' in item:  
        text = item['data']['text']
        output_data["text"].append(text)

        entity_list = []
        for annotation in item.get('annotations', []):  
            for result in annotation['result']:
                entity_text = result['value']['text']
                entity_list.append(entity_text)

        output_data["entities"].append(entity_list)

        sentiment_list = []
        for annotation in item.get('annotations', []):
            for result in annotation['result']:
                for label in result['value']['labels']:
                    if label == "org-neg":
                        sentiment_list.append("olumsuz")
                    else:
                        sentiment_list.append("nötr")  

        output_data["sentiments"].append(sentiment_list)