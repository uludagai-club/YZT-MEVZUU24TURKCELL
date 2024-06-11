from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

def load_ner_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)
    return ner_pipeline
