from Image.ImageSentiment import load_c3d_sentiment_model, get_gifs_sentiment, download_gifs
from Text.sentiment.TextSentiment import load_finetuned_models, get_texts_sentiment
from Emoji.EmojiSentiment import get_emoji_sentiments, get_emojis_in_sentence
import re

# Global weight for combining emoji and text sentiment. Tweak to prefer emoji or text.
# Recommended value found by search: 0.2 (trust text more than emoji for this eval set)
EMOJI_WEIGHT = 0.2


def load_models():
    """
    Load required Keras models
    :return: image_model, text_model_ensemble
    """
    print("Loading models...")
    image_model = load_c3d_sentiment_model()
    text_model_ensemble = load_finetuned_models()
    print("Finished loading models!\n")
    return image_model, text_model_ensemble


def parse_media(sentences):
    """
    Parse emoji, image url and text from each sentences
    :param sentences: list of sentences
    :return: emojis_list, images_list, texts_list
    """
    emojis_list = []
    images_list = []
    texts_list = []

    for sentence in sentences:
        # Parse media from sentence
        emojis = get_emojis_in_sentence(sentence)
        image_tags = re.search(r'<img>(.*)<\/img>', sentence)
        text = sentence

        if emojis:
            emojis_list.append(emojis)
            for emoji in emojis:
                sentence = sentence.replace(emoji, "")
            text = sentence
        else:
            emojis_list.append(None)

        if image_tags:
            image_tagged = image_tags.group(0)
            image_link = image_tags.group(1)
            images_list.append(image_link)
            text = text.replace(image_tagged, "")
        else:
            images_list.append(None)

        if text:
            texts_list.append(text)
        else:
            texts_list.append(None)

    return emojis_list, images_list, texts_list


def calculate_scores(emojis_list, images_list, texts_list):
    """
    Calculate sentiment scores given lists of media
    Emoji scores are considered first as they are a good indicator of sentiment in a sentence
    Text is considered the next most reliable and the model has a high classification accuracy
    Image is considered the worst and is used as a final option
    :param emojis_list: emojis in sentences
    :param images_list: image urls in sentences
    :param texts_list: texts in sentences
    :return: sentiment_scores
    """
    sentiment_scores = []

    if len(emojis_list) == len(images_list) == len(texts_list):
        for i in range(len(emojis_list)):
            emoji_score = emojis_list[i]
            image_score = images_list[i]
            text_score = texts_list[i]

            # If both emoji and text sentiment are available, combine them
            # using a weighted average. This avoids the emoji completely
            # overriding text (or vice-versa) and yields more accurate
            # predictions for mixed inputs. The weights can be tuned.
            if emoji_score is not None and text_score is not None:
                try:
                    combined = (emoji_score * EMOJI_WEIGHT) + (text_score * (1 - EMOJI_WEIGHT))
                except Exception:
                    combined = emoji_score
                sentiment_scores.append(combined)
            elif emoji_score is not None:
                sentiment_scores.append(emoji_score)
            elif text_score is not None:
                sentiment_scores.append(text_score)
            elif image_score is not None:
                sentiment_scores.append(image_score)
            else:
                sentiment_scores.append(None)
    else:
        print("Lists are not the same size!")

    return sentiment_scores


def _has_positive_emoji(emoji_tokens):
    """Heuristic: does the emoji token list contain clearly positive emojis?"""
    if not emoji_tokens:
        return False
    positive = set(list("😁😀😊🙂😃😄😆😎😍🤗👍🎉❤️💕💖✨🥳😺😸"))
    try:
        # Handle both list of emojis and single emoji string
        if isinstance(emoji_tokens, str):
            emoji_tokens = [emoji_tokens]
        return any((e in positive) for e in emoji_tokens)
    except Exception:
        return False


def _has_soft_negation(text):
    """Detect patterns like 'not (that|so|really) sad|upset|angry|depressed|unhappy|down|bad'"""
    if not text:
        return False
    # Widened pattern: allow optional modifiers and match negative keywords anywhere in phrase
    pattern = re.compile(r"\bnot\s+(?:that\s+|so\s+|really\s+|very\s+|too\s+)?(sad|upset|depressed|angry|mad|unhappy|down|bad)",
                         re.IGNORECASE)
    return bool(pattern.search(text))


def _postprocess_smoothing(initial_scores, original_texts, original_emojis):
    """Apply light post-processing: if score is moderately negative but text has a soft negation
    (e.g., 'not that sad') and emojis are positive, pull score toward neutral.

    This is a conservative adjustment to reduce false negatives on mild-negated phrases.
    """
    if not initial_scores:
        return initial_scores

    smoothed = list(initial_scores)
    for i, score in enumerate(initial_scores):
        try:
            if score is None:
                continue
            # Only adjust moderate negatives
            if -0.6 < score < -0.05:
                text = original_texts[i] if i < len(original_texts) else None
                emojis = original_emojis[i] if i < len(original_emojis) else None
                
                has_negation = _has_soft_negation(text)
                has_pos_emoji = _has_positive_emoji(emojis)
                
                if has_negation and has_pos_emoji:
                    # Pull toward neutral: shrink magnitude and add a small positive bias
                    adjusted = (score * 0.4) + 0.1
                    # Clamp to [-1, 1]
                    adjusted = max(-1.0, min(1.0, adjusted))
                    smoothed[i] = adjusted
        except Exception:
            # On any unexpected issue, keep original score
            pass
    return smoothed


def get_sentiments(sentences, image_model, text_model_ensemble):
    """

    :param sentences:
    :param image_model:
    :param text_model_ensemble:
    :return:
    """
    emojis_list, images_list, texts_list = parse_media(sentences)

    # Preserve originals for post-processing rules (deep copy to avoid overwrite)
    import copy
    original_emojis = copy.deepcopy(emojis_list)
    original_texts = copy.deepcopy(texts_list)

    # get indexes of entries that are not None
    emojis_indexes = [i for i in range(len(emojis_list)) if emojis_list[i] is not None]
    images_indexes = [i for i in range(len(images_list)) if images_list[i] is not None]
    texts_indexes = [i for i in range(len(texts_list)) if texts_list[i] is not None]

    # get entries that are not None
    clean_emojis_list = [emojis_list[i] for i in emojis_indexes]
    clean_images_list = [images_list[i] for i in images_indexes]
    clean_texts_list = [texts_list[i] for i in texts_indexes]

    # get sentiment for entries
    clean_emojis_sentiment = get_emoji_sentiments(clean_emojis_list)
    if clean_images_list and image_model is not None:
        image_paths = download_gifs(clean_images_list, path="downloads")
        if image_paths:
            clean_images_sentiment = get_gifs_sentiment(image_paths, image_model)
        else:
            clean_images_sentiment = []
    else:
        clean_images_sentiment = []
    clean_texts_sentiment = get_texts_sentiment(clean_texts_list, text_model_ensemble)

    # replace entries with sentiment scores
    for i in range(len(clean_emojis_sentiment)):
        emojis_list[emojis_indexes[i]] = clean_emojis_sentiment[i]

    for i in range(len(clean_images_sentiment)):
        images_list[images_indexes[i]] = clean_images_sentiment[i]

    for i in range(len(clean_texts_sentiment)):
        texts_list[texts_indexes[i]] = clean_texts_sentiment[i]

    initial_scores = calculate_scores(emojis_list, images_list, texts_list)

    # Apply light rule-based smoothing for soft negation + positive emoji cases
    final_scores = _postprocess_smoothing(initial_scores, original_texts, original_emojis)
    return final_scores
