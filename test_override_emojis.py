from Emoji.EmojiSentiment import get_emoji_sentiments


def test_overrides_negative():
    # Known sad emojis should produce a negative sentiment (curated overrides)
    emojis = [['😢'], ['😭'], ['😥']]
    scores = get_emoji_sentiments(emojis)
    assert all(s is not None for s in scores), f"Got None in scores: {scores}"
    assert scores[0] < 0, f"Expected negative for 😢 but got {scores[0]}"
    assert scores[1] < 0, f"Expected negative for 😭 but got {scores[1]}"
    assert scores[2] < 0, f"Expected negative for 😥 but got {scores[2]}"


if __name__ == '__main__':
    test_overrides_negative()
    print('test_override_emojis passed')
