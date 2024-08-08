import uvicorn
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from fastapi import FastAPI
from pydantic import BaseModel, Field
# from mevzuu import generate_output
from tools import generate_output_textbase
from model import train_model

def changeForResult(outputs):
  ch_entity_list = []
  ch_results = []

  for output in outputs:
      ch_entity_list.extend(output["entity_list"])
      ch_results.extend(output["results"])

  ch_output = {
      "entity_list": list(set(ch_entity_list)),  
      "results": ch_results
  }

  return ch_output

app = FastAPI()

class Item(BaseModel):
    text: str = Field(..., example="""Fiber 100mb SuperOnline kullanıcısıyım yaklaşık 2 haftadır @Twitch @Kick_Turkey gibi canlı yayın platformlarında 360p yayın izlerken donmalar yaşıyoruz.  Başka hiç bir operatörler bu sorunu yaşamazken ben parasını verip alamadığım hizmeti neden ödeyeyim ? @Turkcell """)

@app.post("/predict/", response_model=dict)
async def predict(item: Item):
  model_name = "dbmdz/bert-base-turkish-cased"
  tokenizer = BertTokenizer.from_pretrained(model_name)
  model = BertForSequenceClassification.from_pretrained(model_name, num_labels=3)
  
  return changeForResult(generate_output_textbase(item.text, model=model, tokenizer=tokenizer))

@app.get("/")
async def read_root():
    return {"message": "YZT | MEVZUU"}


if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)