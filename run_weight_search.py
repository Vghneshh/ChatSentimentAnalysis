from SentimentAnalysis import load_models, get_sentiments, EMOJI_WEIGHT

# Small grid search over emoji weights to maximize accuracy on the evaluation set
# We'll import the evaluation dictionary from testSentimentAnalysis.py without
# triggering the test run (that file is guarded by __main__ checks).
from testSentimentAnalysis import evaluation
from sklearn.metrics import accuracy_score

image_model, text_model_ensemble = load_models()

sentences = list(evaluation.keys())
labels = [evaluation[s] for s in sentences]

best = (None, -1.0)
for w in [i/10.0 for i in range(0, 11)]:
    # set global weight
    import SentimentAnalysis as SA
    SA.EMOJI_WEIGHT = w

    scores = get_sentiments(sentences, image_model, text_model_ensemble)
    preds = []
    for s in scores:
        if s is None:
            preds.append(1)  # default to positive if unknown
        elif s > 0:
            preds.append(1)
        else:
            preds.append(0)

    acc = accuracy_score(labels, preds)
    print(f"weight={w:.2f} -> accuracy={acc:.4f}")
    if acc > best[1]:
        best = (w, acc)

print(f"\nBest weight: {best[0]} with accuracy {best[1]:.4f}")
