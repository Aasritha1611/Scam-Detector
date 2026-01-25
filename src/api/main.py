from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

from src.features.feature_extractor import extract_features

app = FastAPI()

model = joblib.load("models/model.pkl")

class JobText(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "API running"}

@app.post("/predict")
def predict(data: JobText):
    features = extract_features(data.text)
    X = pd.DataFrame([features])

    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0][1]

    return {
        "is_scam": bool(pred),
        "scam_probability": round(prob * 100, 2),
        "trust_score": int((1 - prob) * 100)
    }