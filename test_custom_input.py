#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interactive sentiment analysis - takes input from user at runtime
"""

from SentimentAnalysis import load_models, get_sentiments
import sys
import io

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')

def get_sentiment_label(score):
    """Convert sentiment score to label"""
    if score is None:
        return "No sentiment detected", "N/A"
    
    if score > 0.5:
        return "Very Positive", f"{score:.4f}"
    elif score > 0.2:
        return "Positive", f"{score:.4f}"
    elif score > -0.2:
        return "Neutral", f"{score:.4f}"
    elif score > -0.5:
        return "Negative", f"{score:.4f}"
    else:
        return "Very Negative", f"{score:.4f}"

def analyze_single_input(text, image_model, text_model_ensemble):
    """Analyze a single text input"""
    sentiments = get_sentiments([text], image_model, text_model_ensemble)
    score = sentiments[0]
    label, score_str = get_sentiment_label(score)
    return label, score_str, score

def interactive_mode():
    """
    Interactive mode - takes input from user
    """
    print("="*60)
    print("INTERACTIVE SENTIMENT ANALYSIS")
    print("="*60)
    print()
    print("This tool analyzes sentiment from your text input.")
    print("You can enter text with or without emojis.")
    print()
    print("Commands:")
    print("  - Type 'quit' or 'exit' to stop")
    print("  - Type 'clear' to clear the screen")
    print("  - Type 'help' for more information")
    print("  - Press Enter with empty input to analyze multiple texts")
    print()
    print("="*60)
    print()
    
    # Load models once at startup
    print("Loading models (this may take a moment)...")
    image_model, text_model_ensemble = load_models()
    print("Models loaded successfully!")
    print()
    print("="*60)
    print("Ready! Enter your text below:")
    print("="*60)
    print()
    
    input_count = 0
    
    while True:
        try:
            # Get user input
            user_input = input("> ").strip()
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print()
                print("="*60)
                print(f"Thank you! Analyzed {input_count} input(s).")
                print("="*60)
                break
            
            if user_input.lower() == 'clear':
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                print("="*60)
                print("Ready! Enter your text below:")
                print("="*60)
                print()
                continue
            
            if user_input.lower() == 'help':
                print()
                print("Help:")
                print("  - Enter any text with or without emojis")
                print("  - Examples: 'I love this! 😍', 'This is bad 😢'")
                print("  - Type 'quit' to exit")
                print("  - Type 'clear' to clear screen")
                print()
                continue
            
            # Skip empty input
            if not user_input:
                continue
            
            # Analyze the input
            label, score_str, score = analyze_single_input(user_input, image_model, text_model_ensemble)
            input_count += 1
            
            # Display result
            print()
            print("-" * 60)
            print(f"Input: {user_input}")
            print(f"Sentiment Score: {score_str}")
            print(f"Sentiment: {label}")
            print("-" * 60)
            print()
            
        except KeyboardInterrupt:
            print()
            print()
            print("="*60)
            print(f"Interrupted. Analyzed {input_count} input(s).")
            print("="*60)
            break
        except Exception as e:
            print()
            print(f"Error: {str(e)}")
            print("Please try again.")
            print()

def batch_mode():
    """
    Batch mode - analyze multiple inputs at once
    """
    print("="*60)
    print("BATCH SENTIMENT ANALYSIS")
    print("="*60)
    print()
    print("Enter multiple texts (one per line).")
    print("Press Enter twice (empty line) to finish and analyze.")
    print("Type 'quit' to cancel.")
    print()
    print("="*60)
    print()
    
    # Load models
    print("Loading models...")
    image_model, text_model_ensemble = load_models()
    print("Models loaded!")
    print()
    
    # Collect inputs
    inputs = []
    print("Enter your texts (press Enter twice when done):")
    print()
    
    while True:
        try:
            line = input()
            
            if line.lower() == 'quit':
                print("Cancelled.")
                return
            
            if not line.strip():
                # Empty line - check if we have inputs
                if inputs:
                    break
                else:
                    print("No inputs entered. Type 'quit' to cancel or enter text:")
                    continue
            
            inputs.append(line.strip())
            
        except KeyboardInterrupt:
            print("\nCancelled.")
            return
    
    if not inputs:
        print("No inputs to analyze.")
        return
    
    # Analyze all inputs
    print()
    print("="*60)
    print("ANALYZING...")
    print("="*60)
    print()
    
    sentiments = get_sentiments(inputs, image_model, text_model_ensemble)
    
    # Display results
    print("="*60)
    print("RESULTS")
    print("="*60)
    print()
    
    for i, (text, score) in enumerate(zip(inputs, sentiments), 1):
        label, score_str = get_sentiment_label(score)
        print(f"{i}. Text: {text}")
        print(f"   Score: {score_str} ({label})")
        print("-" * 60)
    
    print()
    print(f"Total analyzed: {len(inputs)} input(s)")

def main():
    """Main function - choose mode"""
    print("="*60)
    print("SENTIMENT ANALYSIS - USER INPUT MODE")
    print("="*60)
    print()
    print("Choose mode:")
    print("  1. Interactive mode (analyze one text at a time)")
    print("  2. Batch mode (analyze multiple texts at once)")
    print()
    
    while True:
        try:
            choice = input("Enter choice (1 or 2): ").strip()
            
            if choice == '1':
                interactive_mode()
                break
            elif choice == '2':
                batch_mode()
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            break

if __name__ == '__main__':
    main()

