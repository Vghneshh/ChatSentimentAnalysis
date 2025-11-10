from SentimentAnalysis import load_models, get_sentiments


def test_combined_negative():
    # End-to-end test: sad text + sad emoji should produce a negative score
    image_model, text_model_ensemble = load_models()
    sentences = ["I'm really sad 😢"]
    scores = get_sentiments(sentences, image_model, text_model_ensemble)
    score = scores[0]
    assert score is not None, 'Score is None'
    assert score < 0, f'Expected negative score for sad sentence but got {score}'


if __name__ == '__main__':
    test_combined_negative()
    print('test_combined_negative passed')
