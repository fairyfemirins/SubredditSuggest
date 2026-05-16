# SubredditSuggest
**Autonomously built by Femirins**

A tool to suggest the best subreddits for your post using NLP.

## Features
- CLI interface for quick suggestions.
- Top 3 subreddit suggestions with confidence scores.
- Fetches subreddit metadata via Reddit API (planned).

## Installation
```bash
git clone https://github.com/Femirins/SubredditSuggest.git
cd SubredditSuggest
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage
```bash
python src/cli.py --title "How do I train a neural network?" --content "I'm new to ML..."
```

## Technical Architecture
1. **Data Collection:** `praw` scrapes top 1,000 subreddits (or uses mock data).
2. **NLP Model:** TF-IDF + LogisticRegression trained on subreddit descriptions.
3. **Prediction:** User input → model → top 3 subreddits.

## Limitations
- Reddit API access is mocked due to credential restrictions.
- Model accuracy depends on subreddit metadata quality.

## License
MIT