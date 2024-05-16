# import warnings
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction.text import CountVectorizer
# import nltk
# from textblob import Word
# from transformers import BertTokenizer, BertForSequenceClassification
# from torch.utils.data import DataLoader, TensorDataset
# import torch
# from nltk.sentiment import SentimentIntensityAnalyzer
# import numpy as np

# warnings.filterwarnings('ignore')

# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 200)
# pd.set_option('display.float_format', lambda x: '%.2f' % x)

# df = pd.read_csv('cleaned_reviews.csv')

# df['Görüş'] = df['Görüş'].str.lower()
# df['Görüş'] = df['Görüş'].str.replace(r'\b\w{1,2}\b', '')
# df['Görüş'] = df['Görüş'].str.replace('\d', '')

# sw = nltk.corpus.stopwords.words('turkish')
# df['Görüş'] = df['Görüş'].apply(lambda x: " ".join(x for x in str(x).split() if x not in sw))

# sil = pd.Series(' '.join(df['Görüş']).split()).value_counts()[-1000:]
# df['Görüş'] = df['Görüş'].apply(lambda x: " ".join(x for x in x.split() if x not in sil))

# df['Görüş'] = df['Görüş'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

# sia = SentimentIntensityAnalyzer()
# def label_sentiment(x):
#     compound_score = sia.polarity_scores(x)['compound']
#     if compound_score > 0.25:
#         return "pos"
#     elif -0.25<compound_score < 0.25:
#         return "tarafsız"
#     else:
#         return "neg"
# df['Sentiment_Label'] = df['Görüş'].apply(label_sentiment)

# df.to_csv('labeled_reviews.csv', index=False)

# train_x, test_x, train_y, test_y = train_test_split(df['Görüş'], df['Sentiment_Label'], random_state=42)

# tf_idf_word_vectorizer = TfidfVectorizer().fit(train_x)
# train_x_tf_idf_word = tf_idf_word_vectorizer.transform(train_x)
# test_x_tf_idf_word = tf_idf_word_vectorizer.transform(test_x)

# train_x, test_x, train_y, test_y = train_test_split(df['Görüş'], df['Sentiment_Label'], random_state=42)

# vectorizer = CountVectorizer()
# X_train = vectorizer.fit_transform(train_x)
# X_test = vectorizer.transform(test_x)

# label_mapping = {"pos": 1, "neg": 0}  
# y_train = train_y.map(label_mapping)
# y_test = test_y.map(label_mapping)

# tokenizer = BertTokenizer.from_pretrained("savasy/bert-base-turkish-sentiment-cased")
# train_encodings = tokenizer(list(train_x), padding=True, truncation=True, return_tensors="pt")
# test_encodings = tokenizer(list(test_x), padding=True, truncation=True, return_tensors="pt")

# train_labels = torch.tensor([1 if label == "pos" else 0 for label in train_y])
# test_labels = torch.tensor([1 if label == "pos" else 0 for label in test_y])

# train_dataset = TensorDataset(train_encodings['input_ids'], train_encodings['attention_mask'], train_labels)
# test_dataset = TensorDataset(test_encodings['input_ids'], test_encodings['attention_mask'], test_labels)

# train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
# test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)

# model = BertForSequenceClassification.from_pretrained("savasy/bert-base-turkish-sentiment-cased", num_labels=2)

# def train(model, train_loader, optimizer, criterion, device):
#     model.train()
#     total_loss, total_accuracy = 0, 0
    
#     for batch in train_loader:
#         input_ids, attention_mask, labels = batch
#         input_ids, attention_mask, labels = input_ids.to(device), attention_mask.to(device), labels.to(device)
        
#         optimizer.zero_grad()
#         outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
#         loss = outputs.loss
#         logits = outputs.logits
        
#         loss.backward()
#         optimizer.step()
        
#         total_loss += loss.item()
#         total_accuracy += (logits.argmax(axis=1) == labels).sum().item() / labels.size(0)
    
#     return total_loss / len(train_loader), total_accuracy / len(train_loader)

# def evaluate(model, test_loader, criterion, device):
#     model.eval()
#     total_loss, total_accuracy = 0, 0
    
#     with torch.no_grad():
#         for batch in test_loader:
#             input_ids, attention_mask, labels = batch
#             input_ids, attention_mask, labels = input_ids.to(device), attention_mask.to(device), labels.to(device)

#             outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
#             loss = outputs.loss
#             logits = outputs.logits

#             total_loss += loss.item()
#             total_accuracy += (logits.argmax(axis=1) == labels).sum().item() / labels.size(0)
    
#     return total_loss / len(test_loader), total_accuracy / len(test_loader)

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
# criterion = torch.nn.CrossEntropyLoss()

# for epoch in range(5):
#     train_loss, train_accuracy = train(model, train_loader, optimizer, criterion, device)
#     test_loss, test_accuracy = evaluate(model, test_loader, criterion, device)
    
#     print(f"Epoch {epoch+1}: Train Loss {train_loss:.4f}, Train Accuracy {train_accuracy:.4f}, Test Loss {test_loss:.4f}, Test Accuracy {test_accuracy:.4f}")

# all_preds, all_labels = [], []

# model.eval()
# with torch.no_grad():
#     for batch in test_loader:
#         input_ids, attention_mask, labels = batch
#         input_ids, attention_mask, labels = input_ids.to(device), attention_mask.to(device), labels.to(device)

#         outputs = model(input_ids, attention_mask=attention_mask)
#         logits = outputs.logits
        
#         all_preds.extend(logits.argmax(axis=1).cpu().numpy())
#         all_labels.extend(labels.cpu().numpy())

# print(classification_report(all_labels, all_preds, target_names=["neg", "pos"]))

import warnings
import pandas as pd
import numpy as np
import nltk
from sympy import evaluate
from textblob import Word
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset
import torch
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

df = pd.read_csv('sentiment_analyse/cleaned_reviews.csv')
df['Görüş'] = df['Görüş'].str.lower()
df['Görüş'] = df['Görüş'].str.replace(r'\b\w{1,2}\b', '')
df['Görüş'] = df['Görüş'].str.replace('\d', '')

sw = nltk.corpus.stopwords.words('turkish')

df['Görüş'] = df['Görüş'].apply(lambda x: " ".join(x for x in str(x).split() if x not in sw))
sil = pd.Series(' '.join(df['Görüş']).split()).value_counts()[-1000:]
df['Görüş'] = df['Görüş'].apply(lambda x: " ".join(x for x in x.split() if x not in sil))
df['Görüş'] = df['Görüş'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

sia = SentimentIntensityAnalyzer()
def label_sentiment(x):
    compound_score = sia.polarity_scores(x)['compound']
    if compound_score > 0.25:
        return "pos"
    elif -0.25<compound_score < 0.25:
        return "tarafsız"
    else:
        return "neg"
df['Sentiment_Label'] = df['Görüş'].apply(label_sentiment)

df.to_csv('labeled_reviews.csv', index=False)