import re

SCAM_KEYWORDS = [
    "pay", "fee", "registration", "whatsapp",
    "urgent", "work from home", "data entry"
]

def extract_features(text):
    text = text.lower()

    return {
        "length": len(text),
        "scam_keyword_count": sum(1 for k in SCAM_KEYWORDS if k in text),
        "upfront_payment": int(bool(re.search(r"(pay|fee|₹)", text))),
        "whatsapp_only": int("whatsapp" in text),
        "urgent_words": int("urgent" in text)
    }