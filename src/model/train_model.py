import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

from src.features.feature_extractor import extract_features

df = pd.read_csv("data/dataset.csv")

X = df["text"].apply(extract_features).tolist()
X = pd.DataFrame(X)
y = df["label"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, "models/model.pkl")
print("Model trained and saved")