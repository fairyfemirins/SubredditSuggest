#!/usr/bin/env python3
"""
Fetch top subreddits and their metadata using PRAW.
Output: data/subreddits.json
"""

import json
import praw
from pathlib import Path

# Initialize PRAW (Reddit API)
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",  # Mock for now; replace with real credentials
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="SubredditSuggest/0.1 by Femirins"
)

# Mock data fallback (if API fails)
MOCK_SUBREDDITS = [
    {
        "display_name": "learnpython",
        "title": "Learn Python",
        "description": "A subreddit for learning Python.",
        "subscribers": 1000000,
        "public_description": "For beginners and experts alike."
    },
    {
        "display_name": "MachineLearning",
        "title": "Machine Learning",
        "description": "Advances in machine learning and AI.",
        "subscribers": 3000000,
        "public_description": "Research, papers, and discussions."
    },
    {
        "display_name": "webdev",
        "title": "Web Development",
        "description": "Web development and design.",
        "subscribers": 2000000,
        "public_description": "HTML, CSS, JavaScript, and more."
    }
]

def fetch_top_subreddits(limit=1000):
    """Fetch top subreddits and their metadata."""
    try:
        subreddits = []
        for subreddit in reddit.subreddits.popular(limit=limit):
            subreddits.append({
                "display_name": subreddit.display_name,
                "title": subreddit.title,
                "description": subreddit.description,
                "subscribers": subreddit.subscribers,
                "public_description": subreddit.public_description
            })
        return subreddits
    except Exception as e:
        print(f"[!] API Error: {e}. Using mock data.")
        return MOCK_SUBREDDITS

if __name__ == "__main__":
    data_dir = Path("../data")
    data_dir.mkdir(exist_ok=True)
    
    subreddits = fetch_top_subreddits(limit=1000)
    with open(data_dir / "subreddits.json", "w") as f:
        json.dump(subreddits, f, indent=2)
    
    print(f"[+] Fetched {len(subreddits)} subreddits. Saved to {data_dir / 'subreddits.json'}")