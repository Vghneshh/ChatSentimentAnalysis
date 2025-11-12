"""
Streamlit Frontend for ChatSentimentAnalysis
Multi-modal sentiment analysis with text, emoji, and image support
"""

import streamlit as st
import sys
import os

# Add project paths
sys.path.insert(0, os.path.dirname(__file__))

from SentimentAnalysis import load_models, get_sentiments
import plotly.graph_objects as go
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Chat Sentiment Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .sentiment-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .positive {
        background-color: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
    }
    .negative {
        background-color: #f8d7da;
        color: #721c24;
        border: 2px solid #f5c6cb;
    }
    .neutral {
        background-color: #fff3cd;
        color: #856404;
        border: 2px solid #ffeaa7;
    }
    .stTextInput>div>div>input {
        font-size: 1.1rem;
    }
    .stTextArea textarea {
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
@st.cache_resource
def load_sentiment_models():
    """Load models once and cache them"""
    return load_models()

if 'history' not in st.session_state:
    st.session_state.history = []

def get_sentiment_color(score):
    """Return color based on sentiment score"""
    if score > 0.2:
        return "#28a745"
    elif score < -0.2:
        return "#dc3545"
    else:
        return "#ffc107"

def get_sentiment_label(score):
    """Convert score to label"""
    if score > 0.2:
        return "Positive"
    elif score < -0.2:
        return "Negative"
    else:
        return "Neutral"

def get_sentiment_class(label):
    """Return CSS class based on sentiment label"""
    return label.lower()

def create_gauge_chart(score):
    """Create a gauge chart for sentiment score"""
    label = get_sentiment_label(score)
    # Normalize score to 0-100 range for gauge
    gauge_value = ((score + 1) / 2) * 100
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=gauge_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Sentiment: {label}", 'font': {'size': 24}},
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': get_sentiment_color(score)},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#ffcccc'},
                {'range': [40, 60], 'color': '#ffffcc'},
                {'range': [60, 100], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': gauge_value
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="white",
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_score_breakdown(scores_list, emojis_list, images_list, texts_list):
    """Create bar chart for score breakdown"""
    components = []
    scores = []
    
    # Get individual component scores
    if texts_list and texts_list[0] is not None:
        components.append('Text')
        scores.append(texts_list[0])
    
    if emojis_list and emojis_list[0] is not None:
        components.append('Emoji')
        scores.append(emojis_list[0])
    
    if images_list and images_list[0] is not None and images_list[0] != 0.0:
        components.append('Image')
        scores.append(images_list[0])
    
    if scores_list:
        components.append('Combined')
        scores.append(scores_list[0])
    
    colors = [get_sentiment_color(s) for s in scores]
    
    fig = go.Figure(data=[
        go.Bar(
            x=components,
            y=scores,
            marker_color=colors,
            text=[f"{s:.3f}" for s in scores],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Score Breakdown by Component",
        yaxis_title="Sentiment Score",
        xaxis_title="Component",
        yaxis=dict(range=[-1, 1]),
        height=300,
        showlegend=False
    )
    
    return fig

# Header
st.markdown('<div class="main-header">💬 Chat Sentiment Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-modal sentiment analysis with text, emoji, and image support</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings & Info")
    
    st.markdown("---")
    
    st.header("📊 Model Info")
    st.info("""
    **Text Model:** DeepMoji (Fine-tuned)
    - Twitter: 87.22% accuracy
    - YouTube: 89.13% accuracy
    
    **Emoji Model:** Lexicon-based
    - 1000+ emoji mappings
    - Curated overrides
    
    **Image Model:** C3D (3D-CNN)
    - ~75% accuracy on GIFGIF
    """)
    
    st.markdown("---")
    
    st.header("📖 Features")
    st.markdown("""
    ✅ Text sentiment analysis
    
    ✅ Emoji sentiment analysis
    
    ✅ GIF/Image analysis
    
    ✅ Conflict detection
    - Happy emoji + sad text → neutral
    
    ✅ Negation smoothing
    - "not that sad 😊" → neutral
    
    ✅ Sarcasm handling
    """)

# Main content
tab1, tab2, tab3 = st.tabs(["📝 Analyze", "📊 History", "💡 Examples"])

with tab1:
    # Load models
    with st.spinner('Loading models... This may take a moment on first run.'):
        try:
            image_model, text_model_ensemble = load_sentiment_models()
            st.success("✅ Models loaded successfully!")
        except Exception as e:
            st.error(f"❌ Error loading models: {str(e)}")
            st.stop()
    
    # Input section
    st.header("Enter Text to Analyze")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_area(
            "Type your message here (can include emojis):",
            height=120,
            placeholder="e.g., I'm not that sad today 😊",
            help="Enter text with emojis. For images, include GIF URLs in <img>URL</img> tags"
        )
    
    with col2:
        st.markdown("### Quick Emojis")
        quick_emojis = ["😊", "😢", "😂", "😍", "😡", "😭", "🎉", "👍", "👎"]
        for emoji in quick_emojis:
            if st.button(emoji, key=f"emoji_{emoji}", use_container_width=True):
                user_input += emoji
    
    # GIF URL input (optional)
    gif_url = st.text_input(
        "Optional: Add GIF URL",
        placeholder="https://media.giphy.com/media/XXXXX/giphy.gif",
        help="Enter a direct GIF URL from GIPHY or other sources"
    )
    
    # Analyze button
    if st.button("🔍 Analyze Sentiment", type="primary", use_container_width=True):
        if user_input.strip() or gif_url.strip():
            # Combine text and GIF
            full_input = user_input
            if gif_url.strip():
                full_input += f" <img>{gif_url}</img>"
            
            with st.spinner('Analyzing sentiment...'):
                try:
                    # Run sentiment analysis
                    from SentimentAnalysis import parse_media, calculate_scores
                    from Text.sentiment.TextSentiment import get_texts_sentiment
                    from Emoji.EmojiSentiment import get_emoji_sentiments
                    from Image.ImageSentiment import download_gifs, get_gifs_sentiment
                    
                    # Parse input
                    emojis_list, images_list, texts_list = parse_media([full_input])
                    
                    # Get sentiment for each component
                    text_scores = []
                    emoji_scores = []
                    image_scores = []
                    
                    if texts_list[0]:
                        text_scores = get_texts_sentiment([texts_list[0]], text_model_ensemble)
                        texts_list[0] = text_scores[0]
                    
                    if emojis_list[0]:
                        emoji_scores = get_emoji_sentiments([emojis_list[0]])
                        emojis_list[0] = emoji_scores[0]
                    
                    if images_list[0] and image_model is not None:
                        image_paths = download_gifs([images_list[0]], path="downloads")
                        if image_paths:
                            image_scores = get_gifs_sentiment(image_paths, image_model)
                            images_list[0] = image_scores[0]
                    
                    # Calculate combined score
                    final_scores = calculate_scores(emojis_list, images_list, texts_list)
                    score = final_scores[0] if final_scores else 0.0
                    label = get_sentiment_label(score)
                    
                    # Add to history
                    st.session_state.history.insert(0, {
                        'input': user_input[:100] + "..." if len(user_input) > 100 else user_input,
                        'label': label,
                        'score': score
                    })
                    st.session_state.history = st.session_state.history[:10]
                    
                    # Results section
                    st.markdown("---")
                    st.header("📊 Analysis Results")
                    
                    # Main sentiment display
                    sentiment_class = get_sentiment_class(label)
                    st.markdown(
                        f'<div class="sentiment-box {sentiment_class}">'
                        f'{label} Sentiment'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    
                    # Score display in columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.plotly_chart(
                            create_gauge_chart(score),
                            use_container_width=True
                        )
                    
                    with col2:
                        st.plotly_chart(
                            create_score_breakdown(final_scores, emojis_list, images_list, texts_list),
                            use_container_width=True
                        )
                    
                    # Detailed metrics
                    st.markdown("### 📋 Detailed Breakdown")
                    
                    metrics_cols = st.columns(4)
                    
                    with metrics_cols[0]:
                        st.metric(
                            "🎯 Combined Score",
                            f"{score:.3f}",
                            delta=f"{abs(score):.3f}"
                        )
                    
                    with metrics_cols[1]:
                        if texts_list[0] is not None:
                            st.metric(
                                "📝 Text Score",
                                f"{texts_list[0]:.3f}"
                            )
                    
                    with metrics_cols[2]:
                        if emojis_list[0] is not None:
                            st.metric(
                                "😊 Emoji Score",
                                f"{emojis_list[0]:.3f}"
                            )
                    
                    with metrics_cols[3]:
                        if images_list[0] is not None and images_list[0] != 0.0:
                            st.metric(
                                "🖼️ Image Score",
                                f"{images_list[0]:.3f}"
                            )
                    
                    # Display GIF if provided
                    if gif_url.strip():
                        try:
                            st.markdown("### 🖼️ Analyzed Image")
                            st.image(gif_url, width=300)
                        except:
                            st.warning("Could not display the GIF. Analysis still completed.")
                    
                    st.success("✅ Analysis complete!")
                    
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())
        else:
            st.warning("⚠️ Please enter some text or a GIF URL to analyze.")

with tab2:
    st.header("📊 Analysis History")
    
    if st.session_state.history:
        history_df = pd.DataFrame([
            {
                'Input': h['input'],
                'Label': h['label'],
                'Score': f"{h['score']:.3f}"
            }
            for h in st.session_state.history
        ])
        
        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )
        
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No analysis history yet. Start analyzing to see results here!")

with tab3:
    st.header("💡 Example Inputs to Test")
    
    examples = [
        {
            "title": "✅ Positive with Emoji",
            "input": "I love this so much! 😍",
            "expected": "Positive"
        },
        {
            "title": "❌ Negative with Sad Emoji",
            "input": "I hate this 😢",
            "expected": "Negative"
        },
        {
            "title": "😂 Sarcasm (Conflict Detection)",
            "input": "Oh great, just what I needed 😂",
            "expected": "Neutral (conflict detected)"
        },
        {
            "title": "🔄 Negation Smoothing",
            "input": "I'm not that sad today 😊",
            "expected": "Neutral/Positive (negation smoothed)"
        },
        {
            "title": "😭 Sad Text + Happy Emoji",
            "input": "I am so sad 😁",
            "expected": "Neutral (conflict detected)"
        },
        {
            "title": "💔 Clearly Sad",
            "input": "Feeling devastated and heartbroken 😭",
            "expected": "Negative"
        }
    ]
    
    for i, example in enumerate(examples):
        with st.expander(f"{example['title']}"):
            st.code(example['input'], language=None)
            st.markdown(f"**Expected Result:** {example['expected']}")
            st.markdown("---")
            st.markdown("**Why this works:**")
            if "Conflict" in example['expected']:
                st.info("The system detects when happy emojis conflict with sad text and returns neutral to handle sarcasm/ambiguity.")
            elif "Negation" in example['expected']:
                st.info("The negation smoothing rule detects 'not that sad' patterns and pulls the score toward neutral.")
            elif "Positive" in example['expected']:
                st.success("Clear positive sentiment from both text and emoji.")
            elif "Negative" in example['expected']:
                st.error("Clear negative sentiment from both text and emoji.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ using Streamlit | 
    <a href='https://github.com/Vghneshh/ChatSentimentAnalysis' target='_blank'>GitHub Repository</a>
    </p>
</div>
""", unsafe_allow_html=True)
