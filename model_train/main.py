import json
import pandas as pd
from tools import prepare_data, generate_output, calculate_score, predict_sentiment
from model import train_model, evaluate_model

with open('output_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)

model, tokenizer = train_model(df)
eval_results = evaluate_model(model, tokenizer, df)
# print(f"Değerlendirme Sonuçları: {eval_results}")

output = generate_output(df, model, tokenizer)
# print(json.dumps(output, indent=4, ensure_ascii=False))

ground_truth = df.to_dict("records")
overall_scores = [calculate_score(po, gt) for po, gt in zip(output, ground_truth)]
average_score = sum(overall_scores) / len(overall_scores)
# print(f"Ortalama Skor: {average_score}")