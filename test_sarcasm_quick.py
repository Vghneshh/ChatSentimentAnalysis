#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Quick test for sarcasm detection with laughing emoji."""

from SentimentAnalysis import load_models, get_sentiments_with_components

# Test cases with explicit laughing emojis
test_inputs = [
    "i am dieing right now 😂",
    "This is terrible 😂",
    "Oh great, just what I needed 😂",
    "I'm so done 🤣",
    "This sucks 😆",
]

print("Testing sarcasm detection (laughing emoji + negative text → Neutral):\n")

image_model, text_model = load_models()

for text in test_inputs:
    result = get_sentiments_with_components([text], image_model, text_model)
    r = result[0]
    score = r['combined_score']
    label = r['label']
    text_sc = r['text_score']
    emoji_sc = r['emoji_score']
    def fmt(val):
        try:
            return f"{float(val):.3f}"
        except (TypeError, ValueError):
            return "None"
    print(f"Input: {text}")
    print(f"  Score: {fmt(score)} | Label: {label}")
    print(f"  Text: {fmt(text_sc)} | Emoji: {fmt(emoji_sc)}")
    print()
