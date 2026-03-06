# ChatSentimentAnalysis

Multi-modal sentiment analysis for chat and social media: text, emojis and images (GIFs). This repository combines a DeepMoji-based text model, an emoji sentiment lexicon with curated overrides, and an optional C3D image model to provide robust sentiment scores for chat inputs.

---

## Quick Highlights
- Text sentiment: DeepMoji base model + fine-tuned classifiers for Twitter and YouTube
- Emoji sentiment: curated emoji → sentiment mapping with conservative overrides
- Image sentiment: optional C3D model (GIF/video); disabled if model file is missing
- Multi-modal fusion: weighted average (default emoji weight = 0.2)

## Status
- Text models: finetuned Twitter and YouTube models included (trained, ~157 MB each)
- DeepMoji base weights: included
- Image (C3D) model: optional — not included by default due to size / licensing

## Quick start (Windows PowerShell)
From the project root:

```powershell
# (optional) activate venv
& ".\.venv\Scripts\Activate.ps1"

# Run interactive mode (type inputs)
& ".\.venv\Scripts\python.exe" test_custom_input.py

# Or demo (preconfigured examples)
& ".\.venv\Scripts\python.exe" demo_interactive.py

# Run end-to-end tests
& ".\.venv\Scripts\python.exe" testSentimentAnalysis.py
```

## Files of interest
- `SentimentAnalysis.py` — main fusion logic and entry points
- `Emoji/EmojiSentiment.py` — emoji extraction and mapping
- `Text/sentiment/TextSentiment.py` — loading finetuned models and text scoring
- `Image/ImageSentiment.py` — image/GIF sentiment wrapper (requires C3D model)

## Models & Large Files
Large model files are tracked with Git LFS in this repo. If you clone the repository, ensure Git LFS is installed to fetch the model files:

```powershell
git lfs install
git clone https://github.com/Vghneshh/ChatSentimentAnalysis.git
```

If you prefer not to use LFS, see `RELEASE.md` for alternate download instructions and links.

## Lightweight Web UI (Python 3.6 Fallback)
Streamlit requires Python >= 3.7 and modern versions can fail to install cleanly on legacy 3.6 environments. A dependency‑free fallback server is provided in `server.py` so you can still get a browser UI.

```powershell
# From project root (optional: activate venv if models need it)
& ".\.venv\Scripts\Activate.ps1"

# Start lightweight server (serves at http://127.0.0.1:7860)
python server.py

# Then open your browser:
Start-Process "http://127.0.0.1:7860"
```

API usage example (PowerShell):
```powershell
$body = @{ text = 'I am not that sad today 😊' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:7860/api/analyze -ContentType 'application/json' -Body $body
```

If you later upgrade to Python 3.9+, you can install Streamlit and use the richer `app.py` UI:
```powershell
# After installing a newer Python (e.g., 3.11)
py -3.11 -m venv .venv_streamlit
& ".\.venv_streamlit\Scripts\Activate.ps1"
pip install --upgrade pip
pip install streamlit plotly pandas
streamlit run app.py
```

## Sentiment Rules Enhancements
Beyond raw model scores the system applies post‑fusion heuristics:
1. Emoji/Text Conflict Neutralization: Strongly sad text + clearly happy emoji → Neutral (sarcasm / ambivalence handling).
2. Soft Negation Smoothing: Phrases like "not that sad" pull a mild negative score toward neutral to avoid over‑penalization.
3. Weighted Fusion: Emoji contribution capped (default 0.2 weight) so expressive text dominates without ignoring emojis.
4. Positive Keyword Boost: When the fused score is near zero but text contains clear positive words (e.g., "happy", "awesome"), gently boost toward positive to avoid neutral misclassification on short utterances.

These are implemented in `SentimentAnalysis._postprocess_smoothing`.

## How it works (summary)
- Extract emojis, images and text from input
- Score each modality independently (text: DeepMoji-based classifier; emoji: lookup + fallback; image: C3D)
- Normalize scores to [-1, 1]
- Fuse using weighted average: `final = emoji_score*0.2 + text_score*0.8` (default)

## Algorithms (Detailed)

### Text (DeepMoji Fine-Tuned)
Architecture: Embeddings → 2 BiLSTM (1024 units) → Attention → Dense classifier. Pre-trained on 1.2B tweets (emoji prediction), then fine-tuned on SS-Twitter (≈87%) and SS-YouTube (≈89%). Attention layer highlights sentiment-bearing tokens. Transfer learning reduces overfitting on relatively small labeled sentiment sets.

### Emoji (Lexicon + Overrides)
Primary source: Emoji Sentiment Ranking (mapped 0..1 → −1..1). Overrides applied for strongly negative facial emojis (😢, 😭, 😥, 😓, 😩). Unknown emojis fall back to simple keyword heuristics ("smile", "love" → positive; "cry", "angry" → negative). Fast O(1) lookup, no training required.

### Image / GIF (Optional C3D)
3D CNN (8 conv + 5 pool + 2 FC layers) over 16 uniformly sampled frames (112×112). Captures spatiotemporal emotion cues (facial expression + motion). SGD + momentum (0.9); trained 50 epochs on balanced 5K GIFs (≈75% validation accuracy). Disabled gracefully if model file not present.

### Fusion & Post-Processing
Weighted linear fusion (emoji 0.2, text 0.8) chosen to prevent single high-intensity emoji from overwhelming rich textual context. Post-hoc rules adjust edge cases:
- Conflict (happy emoji + sad text) → neutral
- Soft negation ("not that sad" + positive emoji) → score pulled toward 0
- Positive micro‑utterances near zero ("happy today") → small boost
- Emoticon blocking concept retained conceptually: if text is blank/neutral but emoji is strong, emoji score may dominate.

### Label Thresholds
```
score < -0.2  → Negative
-0.2 ≤ score ≤ 0.2 → Neutral
score > 0.2  → Positive
```
(More granular buckets like "very negative" (< -0.6) or "very positive" (> 0.6) can be layered if needed.)

### Pipeline Pseudocode
```
extract(text) -> emojis, images, plain_text
emoji_score = score_emojis(emojis)
text_score  = score_text(plain_text)  # DeepMoji fine-tuned
image_score = score_images(images)    # C3D (optional)

if plaintext and emojis:
	fused = 0.8*text_score + 0.2*emoji_score
elif emojis_only:
	fused = emoji_score
elif text_only:
	fused = text_score
elif images_only:
	fused = image_score
else:
	fused = 0.0

fused = apply_rules(fused, plain_text, emojis)
label = threshold(fused)
return {score: fused, label, text_sentiment: text_score, emoji_sentiment: emoji_score, image_sentiment: image_score}
```

### Research Gaps / Future Work
- Transformer upgrade (e.g., multilingual sentiment with XLM-R / DistilBERT) for deeper contextual sarcasm handling.
- Dynamic emoji semantics (temporal drift) via continual lexicon re-weighting.
- Joint multi-modal embedding (late fusion now; explore early fusion / attention over modalities).
- Domain adaptation (finance, healthcare chatter) using unsupervised fine-tuning.
- More rigorous sarcasm classifier benchmarking vs current heuristic conflict rule.
- Persistent history + anonymized telemetry for real-world calibration.

### Rationale Summary Table
| Component | Technique | Strength | Trade-off |
|-----------|-----------|----------|-----------|
| Text | BiLSTM + Attention (DeepMoji) | Robust emoji-informed semantics | Larger model size (RAM) |
| Emoji | Lexicon + overrides | Deterministic, fast | Limited nuance / drift |
| Image | 3D CNN (C3D) | Captures motion emotion | Optional, heavy model |
| Fusion | Weighted average + rules | Interpretable | Hand-tuned weights |
| Smoothing | Heuristics | Fix edge misclassifications | Requires manual curation |


## Tests
- Unit tests and small regression checks are included. Run with Python's unittest:

```powershell
& ".\.venv\Scripts\python.exe" -m unittest discover -v
```

## License & Citation
This project uses and adapts the DeepMoji model (Felbo et al., 2017). See `Text/deepmoji.egg-info/PKG-INFO` for license details of that component. The repo code is provided as-is; include appropriate citations if used in research.

---

If you want, I can: add a short project badge, create a GitHub Release with model assets, or scaffold a GitHub Actions workflow to run tests on push.
# ChatSentimentAnalysis
![main](https://i.imgur.com/zyKgSBZ.png)

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org) 
![Python](https://img.shields.io/badge/python-3.6-orange.svg)

> Sentiment analysis of chat data including text, smileys, emojis and images (gifs) with the included difficuly of sarcasm.

> Emoji sentiment using [Emoji Sentiment Ranking](http://kt.ijs.si/data/Emoji_sentiment_ranking/).

> Image sentiment using [C3D](https://gist.github.com/albertomontesg/d8b21a179c1e6cca0480ebdf292c34d2), a 3D-CNN.

> Text sentiment using [DeepMoji](https://github.com/bfelbo/DeepMoji) finetuned on [SS-YouTube and SS-Twitter](https://pdfs.semanticscholar.org/ec1d/92b3b01421e4f49da52fbcf96b9a9337002b.pdf).

---
## Table of Contents
- [Installation](#installation)
- [SentimentAnalysis.py](#SentimentAnalysis.py)
- [Emoji](#Emoji)
- [Image](#Image)
- [Text](#team)
- [Performance](#performance)
- [FAQ](#faq)
- [Support](#support)
- [Additional Notes](#additionalnotes)


---


## Installation
- Download [DeepMoji SS-Twitter Keras Model](https://drive.google.com/open?id=1ZLD2iSgl4PggYPAG9iG_eoFx2DEegqSL) and [DeepMoji SS-YouTube Keras Model](https://drive.google.com/open?id=1iWc0sUmk7FwXBFPQ8FOIWKhJ8jS2iplh) and place them in ```SentimentAnalysis/Text/sentiment/finetuned```.

- Download [DeepMoji Weights](https://www.dropbox.com/s/xqarafsl6a8f9ny/deepmoji_weights.hdf5?dl=0) and place them in ```SentimentAnalysis/Text/model```.

- Download [C3D Sentiment Model](https://drive.google.com/open?id=1UeEsQYrItUF0NOpD1frvS8qxdqGCUTg9) and place in ```SentimentAnalysis/Image```.

## SentimentAnalysis.py
- See testSentimentAnalysis.py for an example.
- Main implementation of sentiment analysis.

## Emoji
![emoji](https://i.imgur.com/P2tMRtJ.png)
- See testEmojiSentiment.py for an example.
- EmojiSentiment.py: Extract sentiment from emojis.
- config.py: Contains emoji to sentiment mappings.
- build: Build files used to generate emoji sentiment mappings.

## Image
- See testImageSentiment.py for an example.
- ImageSentiment.py: Extract sentiment from images(gifs).
- training: Files related to training the classification model.

## Text
![text](https://imgur.com/oXE5H2W.png)
- See testTextSentiment.py for an example.
- Contains modified version of [DeepMoji Python 3](https://github.com/zzsza/DeepMoji-Python3) repo.
- sentiment/TextSentiment.py: Extract sentiment from text and smileys.
- sentiment/build: Example of manualy entered training data for finetuning.
- sentiment/finetuned: Finetuned Keras models used for classification. 

## Performance
 - Performance of the model was tested on 100 tweets containing emojis from [this](https://www.kaggle.com/rexhaif/emojifydata-en) dataset.
 - [This paper](https://www.sciencedirect.com/science/article/pii/S0950705117304240) showed that emoticon blocking (using emoji sentiment as overall sentiment indicator for a sentence) proved to be an effective method of sentiment detection. 
 - This was tested and the results can be observed below.
### Emoticon Blocking
![emoticon-blocking](https://i.imgur.com/Sm3NUnQ.png)
 
 ### Text Only
 ![text-first](https://i.imgur.com/Uj7Bly0.png)

- Emoticon blocking appears to perform better on this small dataset which would suggest it would also perform better on a larger dataset. 
- Emoticon blocking also handles sarcasm where, for example, ```I hate it when you do that 😉``` is considered positive overall, where as it would be classified as negative if only the text was considered.

### C3D Image Sentiment Model
![accuracy](https://i.imgur.com/7Nx6BNi.png)
- 5000 images used in training with 2500 of each class.
- Model trained and evaluated on balanced data set using a training/validation split of 70/30.
- Below is an example of the top negative and positive images from the validation data.

#### Top Negative
![neg1](https://i.imgur.com/WR0C6Qq.gif) ![neg2](https://i.imgur.com/ios7EqN.gif) ![neg3](https://i.imgur.com/vGWhWhS.gif) ![neg4](https://i.imgur.com/yauDFtM.gif) ![neg5](https://i.imgur.com/s275CbK.gif) ![neg6](https://i.imgur.com/DqI48vB.gif) ![neg7](https://i.imgur.com/OLffiZ5.gif) ![neg8](https://i.imgur.com/jkOkrUo.gif)



#### Top Positive
![1pos](https://i.imgur.com/6D351qa.gif) ![pos2](https://i.imgur.com/qywFKc8.gif) ![pos3](https://i.imgur.com/g8Ln6bj.gif) ![pos4](https://i.imgur.com/4KCDcMe.gif) ![pos5](https://i.imgur.com/26KSllL.gif) ![pos6](https://i.imgur.com/tbuNFFS.gif) ![pos7](https://i.imgur.com/keGjqkC.gif) ![pos8](https://i.imgur.com/d7srKWA.gif)

## FAQ

- **How is sentiment calculated?**
	- Text, emojis and images are extracted from a chat sentence like the example given below.
    - ```we lost 😒 😅 😛 <img>https://media.giphy.com/media/2rtQMJvhzOnRe/giphy.gif</img>```
	- Sentiment for each is calculated and a score is returned based on the rules in SentimentAnalysis.calculate_scores().

- **How was the image model trained?**
	- The [C3D Model](https://gist.github.com/albertomontesg/d8b21a179c1e6cca0480ebdf292c34d2) was finetuned using imges from GIPHY.
	- Labelled GIPHY images were obtained from [GIFGIF](http://gifgif.media.mit.edu/labs/api).
	- An R script to extract the  links from JSON has been included in this project. 
	- Text files are generated containing links to the images which can be downloaded from terminal using ```cat file_name.txt | parallel --gnu "wget {}"```.
	- Or the exact files used for training and validation can be downloaded [here](https://drive.google.com/open?id=117xkFzY2OiYMjf6PTPsKYSXENXnPIZVR).

- **Why is there no sentiment score for some emojis?**
	- In my opinion, not all emojis are good indicators of sentiment. 
	- Only emojis with obvious indicators of sentiment such as facial expressions, popular symbols and hand signs were used. 

- **But what about sarcasm detection?**
	- [*DeepMoji has learned to understand emotions and sarcasm based on millions of emojis*](https://deepmoji.mit.edu/).
	- Whether the text contains sarcasm or not is irrelevant, the features extracted using DeepMoji still accurately represent the emotions in the text. These features are used when finetuning new models. 
	- Using emoticon blocking also helps to calculate the actual sentiment in cases of sarcasm e.g. ```I hate it when you do that 😉``` is actually positive and contains a positive emoji but negative text.  Emoticon blocking considers the emoji as the overall sentiment which would be correct in this case.

- **Why was the model only evaluated on combinations of emojis and text?**
	- The sentiment of images is only used if there is no sentiment available for emojis or text in a sentence. The accuracy of this is the same as when the image model was evaluated individually.

---

## Support
Email: `oisin097@hotmail.com`

---


## Additional Notes
- Sentiment analysis from sarcasm detection could be directly tackled using DeepMoji. DeepMoji  outlined in their paper to have been finetuned on [SCv2-GEN](https://arxiv.org/pdf/1709.05404.pdf) to perform sarcasm detection at 75% accuracy. Text could be first passed through this model to detect sarcasm and then the sarcastic sentences passed to another model finetuned on sentiment labelled sentences containing sarcasm. 

- In my opinion, this approach would not be very accurate as the compounding decrease in classification accuracy (is this sarcastic? -> is this positive/negative?) (75% x ??%) would most likely result in a poor result. There is also an increase in computational overhead which enforces the fact this trade off would most li