#!/usr/bin/env python3
"""
CLI tool to suggest subreddits for a post.
Usage: python src/cli.py --title "Your post title" --content "Optional post content"
"""

import click
import pickle
from pathlib import Path
from train_model import preprocess_text

# Mock model fallback
class MockModel:
    def predict(self, texts):
        return ["learnpython", "MachineLearning", "datascience"]
    def predict_proba(self, texts):
        return [[0.4, 0.35, 0.25]]

def load_model():
    """Load the trained model or use mock."""
    try:
        with open("../data/model.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        print(f"[!] Error loading model: {e}. Using mock model.")
        return MockModel()

@click.command()
@click.option("--title", required=True, help="Post title")
@click.option("--content", default="", help="Optional post content")
def suggest_subreddits(title, content):
    """Suggest subreddits for a post."""
    model = load_model()
    text = preprocess_text(title + " " + content)
    
    predictions = model.predict([text])
    probabilities = model.predict_proba([text])
    
    # Handle both mock and trained models
    if isinstance(predictions[0], str):
        subreddit_names = predictions
    else:
        # Extract class labels from the model
        class_labels = model.named_steps["clf"].classes_
        subreddit_names = [class_labels[idx] for idx in predictions]
    
    click.echo("\nTop 3 Subreddit Suggestions:")
    for i, (subreddit, prob) in enumerate(zip(subreddit_names[:3], probabilities[0][:3])):
        click.echo(f"{i+1}. r/{subreddit} (Confidence: {prob:.2f})")

if __name__ == "__main__":
    suggest_subreddits()