import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

df = pd.read_csv("data/dataset_large.csv")

X = df["text"]
y = df["label"]

# Train a TF-IDF + Logistic Regression Pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=1000)),
    ('clf', LogisticRegression(random_state=42))
])

pipeline.fit(X, y)

joblib.dump(pipeline, "models/model.pkl")
print("TF-IDF + Logistic Regression Model trained and saved!")