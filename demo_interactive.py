"""Demo runner to simulate interactive sentiment inputs without needing keyboard interaction.
It prints labels and scores for provided sample inputs.
"""
from SentimentAnalysis import load_models, get_sentiments

DEFAULT_INPUTS = [
    "I'm so sad today 😢",
    "This is great! 🎉",
    "You made me laugh 😂",
    "I hate this so much 😭",
    "I'm sad 😢 but trying to stay positive 🙂",
]


def run_demo(inputs=None):
    if inputs is None:
        inputs = DEFAULT_INPUTS

    image_model, text_model_ensemble = load_models()
    scores = get_sentiments(inputs, image_model, text_model_ensemble)

    def label(score):
        if score is None:
            return "No sentiment"
        if score > 0.5:
            return "Very Positive"
        if score > 0.2:
            return "Positive"
        if score >= -0.2:
            return "Neutral"
        if score >= -0.5:
            return "Negative"
        return "Very Negative"

    print("\nDemo results:\n")
    for txt, sc in zip(inputs, scores):
        print(f"{txt}\n  -> score={sc}\n  -> label={label(sc)}\n")


if __name__ == '__main__':
    run_demo()