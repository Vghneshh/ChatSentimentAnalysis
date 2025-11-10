"""Finetuning script for Twitter model.

Trains the DeepMoji model on the SS-Twitter dataset, using the 'last'
finetuning method and the accuracy metric.

This will create the missing twitter_ss.hdf5 model file.
"""

from __future__ import print_function
import sys
import os

# Add Text directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Text'))

import json
from deepmoji.model_def import deepmoji_transfer
from deepmoji.global_variables import PRETRAINED_PATH
from deepmoji.finetuning import (
     load_benchmark,
     finetune)

DATASET_PATH = 'Text/data/SS-Twitter/raw.pickle'
OUTPUT_PATH = 'Text/sentiment/finetuned/twitter_ss.hdf5'
nb_classes = 2

print("=" * 60)
print("Training Twitter Sentiment Model")
print("=" * 60)
print()

# Check if base weights exist
if not os.path.exists(PRETRAINED_PATH):
    print(f"ERROR: Base weights not found at {PRETRAINED_PATH}")
    print("Please ensure deepmoji_weights.hdf5 is in Text/model/")
    sys.exit(1)

# Check if training data exists
if not os.path.exists(DATASET_PATH):
    print(f"ERROR: Training data not found at {DATASET_PATH}")
    sys.exit(1)

print(f"Loading vocabulary...")
with open('Text/model/vocabulary.json', 'r') as f:
    vocab = json.load(f)

print(f"Loading dataset from {DATASET_PATH}...")
# Load dataset.
data = load_benchmark(DATASET_PATH, vocab)

print(f"Setting up model...")
# Set up model and finetune
model = deepmoji_transfer(nb_classes, data['maxlen'], PRETRAINED_PATH)
model.summary()

print()
print("Starting training...")
print("This may take several hours depending on your hardware.")
print()

model, acc = finetune(model, data['texts'], data['labels'], nb_classes,
                      data['batch_size'], method='last')

print()
print("=" * 60)
print(f"Training complete! Accuracy: {acc}")
print("=" * 60)

# Save the model
print(f"Saving model to {OUTPUT_PATH}...")
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
model.save(OUTPUT_PATH)
print(f"Model saved successfully!")

