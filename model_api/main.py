from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import nltk
from ner import load_ner_model
from fastapi.responses import JSONResponse

app = FastAPI()

nltk.download('punkt')

ner_pipeline = load_ner_model("savasy/bert-base-turkish-ner-cased")
sentiment_pipeline = pipeline("sentiment-analysis", model="savasy/bert-base-turkish-sentiment-cased")

class TextInput(BaseModel):
    text: str

@app.get("/predict/health")
async def health_check():
    return JSONResponse(content={"status": "OK"}, status_code=200)

@app.post("/predict/setup")
async def setup():
    return JSONResponse(content={"status": "Setup completed"}, status_code=200)

@app.post("/predict/")
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