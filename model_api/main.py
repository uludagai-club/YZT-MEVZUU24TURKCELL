from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import nltk

app = FastAPI()

ner_model_name = "savasy/bert-base-turkish-ner-cased"
sentiment_model_name = "savasy/bert-base-turkish-sentiment-cased"

tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name)
ner_pipeline = pipeline("ner", model=ner_model, tokenizer=tokenizer, grouped_entities=True)
sentiment_pipeline = pipeline("sentiment-analysis", model=sentiment_model_name)

nltk.download('punkt')

class TextInput(BaseModel):
    text: str

@app.post("/process/")
async def process_text(input: TextInput):
    text = input.text

    sentences = nltk.sent_tokenize(text)
    results = []
    entity_list = set()

    for sentence in sentences:
        ner_results = ner_pipeline(sentence)
        entities = set([result['word'] for result in ner_results])
        entity_list.update(entities)
        
        for entity in entities:
            entity_occurrences = sentence.split(entity)
            for occurrence in entity_occurrences:
                sentiment_results = sentiment_pipeline(occurrence + entity)
                sentiment = sentiment_results[0]['label']
                
                results.append({"entity": entity, "sentence": occurrence + entity, "sentiment": sentiment})

    output = {
        "entity_list": list(entity_list),
        "results": results
    }
    
    return output
