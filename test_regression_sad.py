import unittest
from SentimentAnalysis import load_models, get_sentiments

class TestSadCombinations(unittest.TestCase):
    def setUp(self):
        # Load models once
        self.image_model, self.text_model_ensemble = load_models()

    def test_sad_emoji_text_are_negative(self):
        # A conservative regression: at least 4 of the 6 sad examples should be
        # classified as negative (score < -0.2). This tolerates a small number
        # of edge cases while still guarding against regressions.
        test_inputs = [
            "I'm so sad today 😢",
            "This makes me cry 😭",
            "Feeling terrible 😔",
            "Bad news 😞",
            "This is awful 😫",
            "Having a rough day 😩",
        ]
        scores = get_sentiments(test_inputs, self.image_model, self.text_model_ensemble)

        negative_count = 0
        for inp, sc in zip(test_inputs, scores):
            # Fail if no sentiment detected
            self.assertIsNotNone(sc, msg=f"No sentiment for input: {inp}")
            if sc < -0.2:
                negative_count += 1

        # Expect the majority of sad examples to be negative
        self.assertGreaterEqual(negative_count, 4,
                                msg=f"Too few negative predictions: {negative_count}/6 (scores={scores})")

if __name__ == '__main__':
    unittest.main()
