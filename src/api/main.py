from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path

from src.features.feature_extractor import get_reasons

app = FastAPI()

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("models/model.pkl")

class JobText(BaseModel):
    text: str

@app.post("/predict")
def predict(data: JobText):
    text = data.text.strip()
    
    if not text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
        
    if len(text) < 10:
        raise HTTPException(status_code=400, detail="Input text is too short to analyze.")

    if len(set(text)) < 5:
        raise HTTPException(status_code=400, detail="Input looks like spam or repeated characters.")

    X = pd.Series([text])

    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0][1]
    
    reasons = get_reasons(text)
    
    if pred == 1 and not reasons:
        reasons.append("Model detected subtle linguistic patterns common in scams.")

    return {
        "is_scam": bool(pred),
        "scam_probability": round(prob * 100, 2),
        "trust_score": int((1 - prob) * 100),
        "message": "Warning: Potential Scam Detected!" if pred else "Content Appears Safe.",
        "reasons": reasons
    }

# Mount static files at the root
web_dir = Path("src/ui/web")
web_dir.mkdir(parents=True, exist_ok=True)
app.mount("/", StaticFiles(directory="src/ui/web", html=True), name="web")