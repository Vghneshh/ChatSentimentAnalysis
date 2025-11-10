import emoji as emoji_library
from Emoji.config import emoji2sentiment

# Curated overrides for specific emojis that should always map to a clear
# negative sentiment. This is a small, conservative list to fix obvious
# mismatches from the original dataset mapping.
EMOJI_OVERRIDES = {
    '😢': -0.8,
    '😭': -0.8,
    '😥': -0.6,
    '😓': -0.6,
    '😩': -0.6,
}


def get_emojis_in_sentence(sentence):
    """
    Return list of emojis in sentence
    :param sentence:
    :return: emojis
    """
    emojis = [c for c in sentence if c in emoji_library.UNICODE_EMOJI]
    return emojis


def get_emoji_sentiment_fallback(emoji_char):
    """
    Fallback method to estimate sentiment for unknown emojis
    Uses emoji library to get emoji name and estimates sentiment based on category
    :param emoji_char: emoji character
    :return: estimated sentiment score or None
    """
    try:
        # Try to get emoji name from emoji library
        emoji_name = emoji_library.demojize(emoji_char)
        
        # Estimate sentiment based on emoji name keywords
        name_lower = emoji_name.lower()
        
        # Positive keywords
        positive_keywords = ['smile', 'happy', 'love', 'heart', 'joy', 'laugh', 'good', 'great', 
                           'excellent', 'celebration', 'party', 'star', 'thumbs', 'ok', 'victory',
                           'kiss', 'hug', 'wink', 'grinning', 'clap', 'fireworks', 'trophy']
        
        # Negative keywords
        negative_keywords = ['sad', 'cry', 'angry', 'mad', 'hate', 'disappointed', 'confused', 
                           'worried', 'fear', 'scared', 'tired', 'weary', 'broken', 'skull',
                           'poop', 'bomb', 'gun', 'pistol', 'frown', 'unamused']
        
        # Check for positive indicators
        if any(keyword in name_lower for keyword in positive_keywords):
            return 0.3  # Slightly positive estimate
        
        # Check for negative indicators
        if any(keyword in name_lower for keyword in negative_keywords):
            return -0.3  # Slightly negative estimate
        
        # Neutral for unknown
        return 0.0
    except:
        return None

def get_emoji_sentiments(emojis_list):
    """
    Get average sentiment of emojis given a list containing lists of emojis from each sentence
    Uses fallback method for unknown emojis
    :param emojis_list:
    :return: average_sentiment_list
    """
    sentiment_lists = []
    
    for emoji_list in emojis_list:
        sentiment_list = []
        for emoji in emoji_list:
            # Curated override takes highest precedence
            if emoji in EMOJI_OVERRIDES:
                sentiment = EMOJI_OVERRIDES[emoji]
            else:
                # Try to get sentiment from config
                sentiment = emoji2sentiment.get(emoji)

            # If not found, use fallback method
            if sentiment is None:
                sentiment = get_emoji_sentiment_fallback(emoji)

            if sentiment is not None:
                # Conservative negative override: if emoji name contains
                # clearly negative keywords, force a negative score.
                try:
                    name_lower = emoji_library.demojize(emoji).lower()
                    negative_override_keys = [
                        'sad', 'sadness', 'cry', 'crying', 'sob', 'sobbing', 'tear', 'tears',
                        'disappointed', 'unhappy', 'broken', 'weep', 'weeping', 'angry', 'mad', 'frown'
                    ]
                    if any(k in name_lower for k in negative_override_keys):
                        # Strong-ish negative override to ensure negative polarity
                        sentiment = -0.5
                except Exception:
                    # ignore demojize errors and continue
                    pass

                # The emoji config values are in range [0, 1] (dataset ratio).
                # Convert values from [0,1] -> [-1,1] to match text model output
                # while leaving fallback values (which may already be negative)
                # intact.
                try:
                    # convert numeric config scores (0..1) to -1..1
                    if isinstance(sentiment, (int, float)) and 0.0 <= sentiment <= 1.0:
                        sentiment = (sentiment * 2) - 1
                except Exception:
                    # if conversion fails, keep original sentiment
                    pass

                sentiment_list.append(sentiment)
        
        sentiment_lists.append(sentiment_list)

    average_sentiment_list = []
    for sentiment_list in sentiment_lists:
        if sentiment_list:
            average_sentiment_list.append(sum(sentiment_list) / len(sentiment_list))
        else:
            average_sentiment_list.append(None)

    return average_sentiment_list
