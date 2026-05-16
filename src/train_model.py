#!/usr/bin/env python3
"""
Train an NLP model to suggest subreddits based on post title/content.
Output: data/model.pkl
"""

import json
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Mock data fallback
MOCK_DATA = [
    {"text": "How do I train a neural network?", "subreddit": "MachineLearning"},
    {"text": "Best Python libraries for data science", "subreddit": "learnpython"},
    {"text": "Data science and statistics resources", "subreddit": "datascience"}
]

def load_subreddits():
    """Load subreddits from JSON or use mock data."""
    try:
        with open("../data/subreddits.json", "r") as f:
            subreddits = json.load(f)
        return subreddits
    except Exception as e:
        print(f"[!] Error loading subreddits: {e}. Using mock data.")
        return MOCK_DATA

def preprocess_text(text):
    """Preprocess text using spaCy."""
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

def train_model(subreddits):
    """Train a TF-IDF + LogisticRegression model."""
    # Check if mock data is being used
    if "display_name" in subreddits[0]:
        texts = [preprocess_text(item.get("title", "") + " " + item.get("description", "") + " " + item.get("public_description", "")) for item in subreddits]
        labels = [item["display_name"] for item in subreddits]
    else:
        # Legacy mock data structure
        texts = [preprocess_text(item["text"]) for item in subreddits]
        labels = [item["subreddit"] for item in subreddits]
    
    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=1000))
    ])
    model.fit(texts, labels)
    return model

if __name__ == "__main__":
    data_dir = Path("../data")
    data_dir.mkdir(exist_ok=True)
    
    subreddits = load_subreddits()
    model = train_model(subreddits)
    
    with open(data_dir / "model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    print(f"[+] Model trained and saved to {data_dir / 'model.pkl'}")