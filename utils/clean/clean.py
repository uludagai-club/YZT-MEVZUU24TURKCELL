import re
import pandas as pd

turkish_chars = str.maketrans(
    "çğıöşüÇĞİÖŞÜ",
    "cgiosuCGIOSU"
)

def clear_text(text):
    text = text.translate(turkish_chars)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d', '', text)
    return text

def read_and_clean(file_path, will_be_clean_columns,save_path):
    df = pd.read_csv(file_path,delimiter=",",encoding="utf-16 LE")
    
    for will_be_clean_column in will_be_clean_columns:
        df[will_be_clean_column] = df[will_be_clean_column].astype(str).apply(clear_text)
        
    df.to_csv(save_path,index=False)

if __name__=='__main__':
    file_path = 'sentiment_analyse/reviews.csv'
    columns = ['Phrase']

    read_and_clean(file_path, columns, "sentiment_analyse/cleaned_reviews.csv")