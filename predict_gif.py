#!/usr/bin/env python3
"""Small helper: predict sentiment for a single GIF URL + optional text

Usage:
  python predict_gif.py <gif_url> [optional text ...]

Examples:
  python predict_gif.py "https://media.giphy.com/media/XXXXX/giphy.gif" "I'm so sad"

This script uses the project's `SentimentAnalysis` module to load models,
download the GIF temporarily and return the fused sentiment score.
If the image model is missing the image score will be neutral (0.0) but
text+emoji sentiment will still be computed.
"""
from __future__ import print_function
import sys
import math

from SentimentAnalysis import load_models, get_sentiments


def score_to_label(score, neutral_threshold=0.05):
    if score is None:
        return "unknown"
    if score > neutral_threshold:
        return "positive"
    if score < -neutral_threshold:
        return "negative"
    return "neutral"


def usage():
    print("Usage: python predict_gif.py <gif_url> [optional text ...]")
    print("Example: python predict_gif.py \"https://media.giphy.com/media/XXXXX/giphy.gif\" \"I'm so sad\"")


def main(argv):
    if len(argv) < 2:
        usage()
        return 1

    gif_url = argv[1]
    extra_text = " ".join(argv[2:]) if len(argv) > 2 else ""
    sentence = (extra_text + " " + f"<img>{gif_url}</img>").strip()

    print("Loading models (this may take a few seconds)...")
    image_model, text_model_ensemble = load_models()

    # Run sentiment pipeline
    try:
        scores = get_sentiments([sentence], image_model, text_model_ensemble)
    except Exception as e:
        print(f"Error computing sentiment: {e}")
        return 2

    if not scores:
        print("No sentiment returned.")
        return 3

    score = scores[0]
    label = score_to_label(score)

    print("\nResult")
    print("------")
    print(f"Combined score: {score}")
    print(f"Label: {label}")

    # Give a short human-friendly explanation
    if image_model is None:
        print("Note: C3D image model not found. Image sentiment is neutral by default.")

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
