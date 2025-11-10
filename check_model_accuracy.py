#!/usr/bin/env python
"""
Check accuracy of both trained models by loading them and evaluating on test data.
"""
import sys
import os
import json
import pickle

# Add Text directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Text'))

from keras.models import load_model
from deepmoji.attlayer import AttentionWeightedAverage
from deepmoji.sentence_tokenizer import SentenceTokenizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

TWITTER_MODEL_PATH = 'Text/sentiment/finetuned/twitter_ss.hdf5'
YOUTUBE_MODEL_PATH = 'Text/sentiment/finetuned/youtube_ss.hdf5'
TWITTER_DATA_PATH = 'Text/data/SS-Twitter/raw.pickle'
YOUTUBE_DATA_PATH = 'Text/data/SS-Youtube/raw.pickle'
VOCAB_PATH = 'Text/model/vocabulary.json'

def load_data(data_path):
    """Load pickled dataset"""
    with open(data_path, 'rb') as f:
        data = pickle.load(f)
        return data.get('texts', []), data.get('labels', [])

def evaluate_model(model_path, data_path, model_name):
    """Load model and evaluate on dataset"""
    print(f"\n{'='*60}")
    print(f"Evaluating {model_name}")
    print(f"{'='*60}")
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"✗ Model not found at {model_path}")
        return
    
    # Check if data exists
    if not os.path.exists(data_path):
        print(f"✗ Data not found at {data_path}")
        return
    
    try:
        # Load model
        print(f"Loading model from {model_path}...")
        model = load_model(model_path, 
                          custom_objects={'AttentionWeightedAverage': AttentionWeightedAverage})
        
        # Load data
        print(f"Loading test data from {data_path}...")
        X_test, y_test = load_data(data_path)
        print(f"  Samples: {len(X_test)}")
        
        # Load tokenizer and vocab
        with open(VOCAB_PATH, 'r') as f:
            vocab = json.load(f)
        
        st = SentenceTokenizer(vocab, 30)
        X_test_encoded, _, _ = st.tokenize_sentences(X_test)
        
        # Make predictions
        print(f"Making predictions...")
        predictions = model.predict(X_test_encoded, batch_size=32, verbose=0)
        y_pred = (predictions > 0.5).astype(int).flatten()
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        # Print results
        print(f"\n✓ {model_name} Results:")
        print(f"  Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        
        # File info
        model_size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"  Model size: {model_size_mb:.2f} MB")
        
        return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1}
        
    except Exception as e:
        print(f"✗ Error evaluating {model_name}: {str(e)}")
        return None

def main():
    print("="*60)
    print("Model Accuracy Checker")
    print("="*60)
    
    # Evaluate both models
    twitter_results = evaluate_model(TWITTER_MODEL_PATH, TWITTER_DATA_PATH, "Twitter Model")
    youtube_results = evaluate_model(YOUTUBE_MODEL_PATH, YOUTUBE_DATA_PATH, "YouTube Model")
    
    # Summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")
    
    if twitter_results:
        print(f"Twitter Model Accuracy:  {twitter_results['accuracy']:.4f} ({twitter_results['accuracy']*100:.2f}%)")
    else:
        print("Twitter Model: Failed to evaluate")
    
    if youtube_results:
        print(f"YouTube Model Accuracy:  {youtube_results['accuracy']:.4f} ({youtube_results['accuracy']*100:.2f}%)")
    else:
        print("YouTube Model: Failed to evaluate")
    
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
