import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

df = pd.read_csv("../dataset/fake_news.csv")

X = df['text']
y = df['label']

vectorizer = TfidfVectorizer(max_features=5000)
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

joblib.dump(model, "../models/text_model.pkl")
joblib.dump(vectorizer, "../models/vectorizer.pkl")