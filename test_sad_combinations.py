#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test sad emoji + sad text combinations
"""

from SentimentAnalysis import load_models, get_sentiments

def test_sad_combinations():
    """Test combinations of sad emojis with sad text"""
    test_inputs = [
        "I'm so sad today 😢",
        "This makes me cry 😭",
        "Feeling terrible 😔",
        "Bad news 😞",
        "This is awful 😫",
        "Having a rough day 😩",
        # Mixed emoji tests
        "I'm sad 😢 but trying to stay positive 🙂",
        "Bad news 😭 but we'll get through this ✨",
        # Control cases
        "I'm happy today 😊",
        "Great news! 🎉",
    ]
    
    print("="*60)
    print("Testing Sad Emoji + Text Combinations")
    print("="*60)
    
    # Load models
    print("\nLoading models...")
    image_model, text_model_ensemble = load_models()
    print("Models loaded!")
    print()
    
    # Get sentiment scores
    scores = get_sentiments(test_inputs, image_model, text_model_ensemble)
    
    # Print results
    print("Results:")
    print("-"*60)
    for text, score in zip(test_inputs, scores):
        sentiment = "Negative" if score < -0.2 else "Neutral" if -0.2 <= score <= 0.2 else "Positive"
        print(f"{text:40} | {score:8.4f} | {sentiment}")

if __name__ == "__main__":
    test_sad_combinations()