import re

def get_reasons(text):
    """
    Reason Engine: analyzes text and returns human-readable reasons
    for why a text might be considered a scam.
    """
    text_lower = text.lower()
    reasons = []
    
    # 1. Payment request
    if re.search(r"(pay|fee|₹|\$|refundable|transfer|vendor)", text_lower):
        reasons.append("Contains upfront payment or financial request.")
        
    # 2. Urgency language
    if re.search(r"(urgent|immediately|quick|now|hurry)", text_lower):
        reasons.append("Uses urgency language commonly found in scams.")
        
    # 3. Unofficial comms
    if re.search(r"(whatsapp|telegram|dm)", text_lower):
        reasons.append("Requests communication via unofficial channels (WhatsApp/Telegram).")
        
    # 4. Too good to be true
    if re.search(r"(shocking|secret trick|massive income|unbelievable)", text_lower):
        reasons.append("Contains 'too good to be true' or clickbait claims.")
        
    # 5. Missing domain/contact info (if no email or link is found)
    if not re.search(r"(@[\w.-]+|http|www)", text_lower):
        reasons.append("No official company domain or email detected.")
        
    return reasons