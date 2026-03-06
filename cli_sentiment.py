#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CLI helper that runs sentiment analysis using the project's existing models
and prints a JSON result to stdout.

Usage (Windows PowerShell):
  .\.venv\Scripts\python.exe cli_sentiment.py "your text with emojis 😁" "optional_gif_url"

Output JSON schema:
  {
    "score": float,             # combined score [-1,1]
    "label": "positive|neutral|negative",
    "text_sentiment": float|null,
    "emoji_sentiment": float|null,
    "image_sentiment": float|null
  }
"""
from __future__ import print_function
import json
import sys

from SentimentAnalysis import load_models, get_sentiments_with_components
from Emoji.EmojiSentiment import get_emojis_in_sentence, get_emoji_sentiments


def label_from_score(score, neutral_threshold=0.2):
    if score is None:
        return "neutral"
    if score > neutral_threshold:
        return "Positive"
    if score < -neutral_threshold:
        return "Negative"
    return "Neutral"


def main(argv):
    if len(argv) < 2:
        print(json.dumps({
            "error": "Usage: python cli_sentiment.py <text> [gif_url]"
        }))
        return 1

    text = argv[1]
    gif_url = argv[2] if len(argv) > 2 else ""
    if gif_url:
        text = f"{text} <img>{gif_url}</img>"

    try:
        # Normal path: load models and compute full multi-modal sentiment
        image_model, text_model_ensemble = load_models()
        details = get_sentiments_with_components([text], image_model, text_model_ensemble)
        if details:
            d0 = details[0]
            combined = d0.get('combined_score', 0.0)
            
            # Convert numpy float32 to native Python float for JSON serialization
            def to_native_float(val):
                if val is None:
                    return None
                return float(val)
            
            result = {
                "score": to_native_float(combined),
                "label": label_from_score(combined),
                "text_sentiment": to_native_float(d0.get('text_score')),
                "emoji_sentiment": to_native_float(d0.get('emoji_score')),
                "image_sentiment": to_native_float(d0.get('image_score'))
            }
        else:
            result = {
                "score": 0.0,
                "label": label_from_score(0.0),
                "text_sentiment": None,
                "emoji_sentiment": None,
                "image_sentiment": None
            }
    except Exception:
        # Fallback: if heavy models fail to load (e.g., old TF/Keras not available),
        # compute emoji-only sentiment so Streamlit UI remains usable.
        emojis = get_emojis_in_sentence(text)
        emoji_score = None
        if emojis:
            scores = get_emoji_sentiments([emojis])
            if scores and scores[0] is not None:
                emoji_score = float(scores[0])
        result = {
            "score": float(emoji_score) if emoji_score is not None else 0.0,
            "label": label_from_score(emoji_score if emoji_score is not None else 0.0),
            "text_sentiment": None,
            "emoji_sentiment": emoji_score,
            "image_sentiment": None
        }
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))