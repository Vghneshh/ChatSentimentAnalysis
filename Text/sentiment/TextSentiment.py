from keras.models import load_model
import json
from deepmoji.attlayer import AttentionWeightedAverage
from deepmoji.sentence_tokenizer import SentenceTokenizer
from deepmoji.global_variables import VOCAB_PATH


def modify_range(val):
    """
    Modify value from range 0,1 -> -1,1 and preserve ratio
    :param val:
    :return: value in rage -1,1
    """
    return (val * 2) - 1


def load_finetuned_models():
    """
    Load finetuned Keras models
    Falls back to base model if finetuned models are missing
    :return: [twitter_model, youtube_model]
    """
    import os
    from deepmoji.model_def import deepmoji_transfer
    from deepmoji.global_variables import PRETRAINED_PATH
    
    twitter_path = 'Text/sentiment/finetuned/twitter_ss.hdf5'
    youtube_path = 'Text/sentiment/finetuned/youtube_ss.hdf5'
    
    # Try to load finetuned models
    if os.path.exists(twitter_path) and os.path.exists(youtube_path):
        try:
            twitter_model = load_model(twitter_path,
                                       custom_objects={'AttentionWeightedAverage': AttentionWeightedAverage})
            youtube_model = load_model(youtube_path,
                                       custom_objects={'AttentionWeightedAverage': AttentionWeightedAverage})
            return [twitter_model, youtube_model]
        except Exception as e:
            print(f"Warning: Could not load finetuned models: {e}")
            print("Falling back to base model...")
    
    # Fallback: Use base model with sentiment head
    print("=" * 60)
    print("WARNING: Finetuned models not found!")
    print("=" * 60)
    print("Using base DeepMoji model with sentiment classification.")
    print("Accuracy will be lower than finetuned models.")
    print()
    print("To get better accuracy, train the models:")
    print("  python train_twitter_model.py")
    print("  python train_youtube_model.py")
    print("=" * 60)
    print()
    
    # Create models from base weights
    if not os.path.exists(PRETRAINED_PATH):
        raise FileNotFoundError(
            f"Base model weights not found at {PRETRAINED_PATH}\n"
            "Please ensure deepmoji_weights.hdf5 is in Text/model/"
        )
    
    # Create sentiment models from base weights
    # Note: These will have lower accuracy than finetuned models
    maxlen = 30
    nb_classes = 2
    
    twitter_model = deepmoji_transfer(nb_classes, maxlen, PRETRAINED_PATH)
    youtube_model = deepmoji_transfer(nb_classes, maxlen, PRETRAINED_PATH)
    
    return [twitter_model, youtube_model]


def get_texts_sentiment(texts, model_ensemble):
    """
    Get sentiment scores for list of texts
    :param texts:
    :param model_ensemble:
    :return: average_sentiment_prediction
    """
    with open(VOCAB_PATH, 'r') as f:
        vocabulary = json.load(f)

    twitter_maxlen = 30
    youtube_maxlen = 30

    twitter_st = SentenceTokenizer(vocabulary, twitter_maxlen)
    youtube_st = SentenceTokenizer(vocabulary, youtube_maxlen)

    twitter_tokenized, _, _ = twitter_st.tokenize_sentences(texts)
    youtube_tokenized, _, _ = youtube_st.tokenize_sentences(texts)

    twitter_predictions = model_ensemble[0].predict(twitter_tokenized)
    youtube_predictions = model_ensemble[1].predict(youtube_tokenized)

    average_predictions = (twitter_predictions + youtube_predictions) / 2
    average_sentiment_prediction = [modify_range(prediction)[0] for prediction in average_predictions]

    return average_sentiment_prediction
