

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
MODEL_NAME = "microsoft/deberta-v3-base"   # 🔥 IMPORTANT

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Recreate model architecture
model = AutoModelForSequenceClassification.from_pretrained(
    "microsoft/deberta-v3-base",
    num_labels=28,   # IMPORTANT: your label count
    problem_type="multi_label_classification"
)

# Load weights
state_dict = torch.load("final_model.pt", map_location=torch.device("cpu"))
model.load_state_dict(state_dict)

model.eval()

# Labels
label_names = ["admiration",  "amusement",    "anger",        "annoyance",
    "approval",    "caring",       "confusion",    "curiosity",
    "desire",      "disappointment","disapproval",  "disgust",
    "embarrassment","excitement",  "fear",         "gratitude",
    "grief",       "joy",          "love",         "nervousness",
    "optimism",    "pride",        "realization",  "relief",
    "remorse",     "sadness",      "surprise",     "neutral"]   # your 28 labels

def predict(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.sigmoid(outputs.logits).cpu().numpy()[0]

    return probs