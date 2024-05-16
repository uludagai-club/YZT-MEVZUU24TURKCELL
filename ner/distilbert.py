from transformers import pipeline, AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("dbmdz/distilbert-base-turkish-cased")
model = AutoModel.from_pretrained("dbmdz/distilbert-base-turkish-cased")

ner=pipeline('ner', model=model, tokenizer=tokenizer)
print(ner("Mustafa Kemal Atatürk 19 Mayıs 1919'da Samsun'a ayak bastı."))