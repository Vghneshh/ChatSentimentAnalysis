import sys
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import subprocess
from pathlib import Path

# Add project to path so we can import directly
sys.path.insert(0, os.path.dirname(__file__))

# Import sentiment analysis directly (faster than subprocess)
try:
    from SentimentAnalysis import load_models, get_sentiments_with_components
    MODELS_LOADED = False
    IMAGE_MODEL = None
    TEXT_MODEL = None
except ImportError as e:
    print(f"Warning: Could not import SentimentAnalysis: {e}")
    MODELS_LOADED = None

# In-memory history for last 10 analyses
HISTORY = []  # each item: {"input": str, "label": str, "score": float, "ts": int}


HTML_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Chat Sentiment Analyzer (Light UI)</title>
  <style>
    body { font-family: Segoe UI, Roboto, Arial, sans-serif; margin: 2rem; }
    h1 { color: #1f77b4; }
    .row { display: flex; gap: 1rem; }
    .tabs { display: flex; gap: 0.5rem; margin: 1rem 0; }
    .tab { padding: 0.5rem 0.9rem; border: 1px solid #ddd; border-bottom: none; border-radius: 6px 6px 0 0; cursor: pointer; background: #f7f7f7; }
    .tab.active { background: #fff; font-weight: 600; }
    .panel { border: 1px solid #ddd; border-radius: 0 6px 6px 6px; padding: 1rem; }
    textarea { width: 100%; height: 120px; font-size: 1rem; }
    input[type="text"] { width: 100%; font-size: 1rem; padding: 0.5rem; }
    button { padding: 0.6rem 1rem; font-size: 1rem; }
    .result { margin-top: 1rem; padding: 1rem; border-radius: 8px; }
    .Positive { background: #d4edda; color: #155724; }
    .Negative { background: #f8d7da; color: #721c24; }
    .Neutral { background: #fff3cd; color: #856404; }
    .small { color: #666; font-size: 0.9rem; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border-bottom: 1px solid #eee; text-align: left; padding: 0.5rem; font-size: 0.95rem; }
    .muted { color: #888; }
  </style>
  <script>
    console.log('✓ Script loading...');
    
    function $(id){ return document.getElementById(id); }
    
    function showTab(tab){
      console.log('showTab called:', tab);
      const tabs = ['analyze','history','examples'];
      tabs.forEach(t => {
        const btn = $('tab_'+t); const pnl = t+'Section';
        if (t===tab){ btn.classList.add('active'); $(pnl).style.display='block'; } else { btn.classList.remove('active'); $(pnl).style.display='none'; }
      });
      if (tab==='history'){ loadHistory(); }
    }

    async function analyze() {
      console.log('analyze() called');
      const text = $('text').value;
      const btn = $('btn');
      const resDiv = $('result');
      if (!text.trim()) {
        resDiv.className = 'result Neutral';
        resDiv.innerHTML = 'Please enter some text';
        return;
      }
      btn.disabled = true; btn.innerText = 'Analyzing…';
      resDiv.innerHTML = '';
      try {
        const res = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });
        const data = await res.json();
        console.log('Analysis result:', data);
        const cls = data.label || 'Neutral';
        const score = (data.score !== undefined) ? data.score.toFixed(3) : '0.000';
        resDiv.className = 'result ' + cls;
        resDiv.innerHTML = `<strong>${cls} Sentiment</strong><br/>Score: ${score}`;
        loadHistory();
      } catch (e) {
        console.error('Analysis error:', e);
        resDiv.className = 'result Neutral';
        resDiv.innerHTML = 'Error: ' + (e.message || e);
      } finally {
        btn.disabled = false; btn.innerText = 'Analyze';
      }
    }

    async function loadHistory(){
      console.log('loadHistory() called');
      try {
        const res = await fetch('/api/history');
        const data = await res.json();
        const tbody = $('histBody');
        tbody.innerHTML = '';
        if (!Array.isArray(data) || data.length===0){
          $('histNone').style.display='block';
          return;
        }
        $('histNone').style.display='none';
        data.forEach(item => {
          const tr = document.createElement('tr');
          const score = (item.score!==undefined && item.score!==null)? Number(item.score).toFixed(3):'—';
          tr.innerHTML = `<td>${escapeHtml(item.input || '')}</td><td>${item.label || '—'}</td><td>${score}</td>`;
          tbody.appendChild(tr);
        });
      } catch(e){ console.warn('history fetch failed', e); }
    }

    function useExample(text){
      console.log('useExample called:', text);
      $('text').value = text;
      showTab('analyze');
    }

    function escapeHtml(str){
      return String(str).replace(/[&<>"] /g, s=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;' }[s]||s));
    }
    
    // Verify functions are defined
    console.log('✓ Functions defined:', {
      showTab: typeof showTab,
      analyze: typeof analyze,
      useExample: typeof useExample
    });
    
    // Add event listeners as backup to onclick
    document.addEventListener('DOMContentLoaded', function() {
      console.log('✓ DOM loaded, attaching event listeners');
      
      // Analyze button
      const btnAnalyze = $('btn');
      if (btnAnalyze) {
        btnAnalyze.addEventListener('click', analyze);
        console.log('✓ Analyze button listener attached');
      } else {
        console.error('✗ Button #btn not found!');
      }
      
      // Tab buttons
      ['analyze', 'history', 'examples'].forEach(tab => {
        const tabBtn = $('tab_' + tab);
        if (tabBtn) {
          tabBtn.addEventListener('click', () => showTab(tab));
          console.log(`✓ Tab ${tab} listener attached`);
        }
      });
      
      // Example buttons - attach listeners to all buttons in examples section
      const exampleBtns = document.querySelectorAll('#examplesSection button');
      console.log(`Found ${exampleBtns.length} example buttons`);
      
      console.log('✓ All event listeners attached. Buttons should work now!');
    });
  </script>
  </head>
<body>
  <h1>💬 Chat Sentiment Analyzer (Light UI)</h1>
  <div class="tabs">
    <div id="tab_analyze" class="tab active">📝 Analyze</div>
    <div id="tab_history" class="tab">📊 History</div>
    <div id="tab_examples" class="tab">💡 Examples</div>
  </div>

  <div class="panel" id="analyzeSection" style="display:block;">
    <p class="small">Text + emoji sentiment analysis.</p>
    <div>
      <label for="text"><strong>Text (emojis allowed):</strong></label><br/>
      <textarea id="text" placeholder="e.g., I'm not that sad today 😊"></textarea>
    </div>
    <div style="margin-top: 1rem;">
      <button id="btn">Analyze</button>
    </div>
    <div id="result" class="result"></div>
    <p class="small">Tip: The first request may take a few seconds while models warm up.</p>
  </div>

  <div class="panel" id="historySection" style="display:none;">
    <h3>📊 Last 10 analyses</h3>
    <div id="histNone" class="small muted" style="display:none;">No history yet.</div>
    <table>
      <thead><tr><th style="width: 70%;">Input</th><th>Label</th><th>Score</th></tr></thead>
      <tbody id="histBody"></tbody>
    </table>
  </div>

  <div class="panel" id="examplesSection" style="display:none;">
    <h3>💡 Example inputs</h3>
    <ul>
      <li>
        <code>I love this so much! 😍</code>
        <div class="small">Strong praise + heart-eyes emoji → Positive</div>
        <button onclick="useExample('I love this so much! 😍')">Use</button>
      </li>
      <li>
        <code>I hate this 😢</code>
        <div class="small">Complaint + sad emoji → Negative</div>
        <button onclick="useExample('I hate this 😢')">Use</button>
      </li>
      <li>
        <code>Oh great, just what I needed 😂</code>
        <div class="small">Sarcasm/ambivalence → Neutral</div>
        <button onclick="useExample('Oh great, just what I needed 😂')">Use</button>
      </li>
      <li>
        <code>I'm not that sad today 😊</code>
        <div class="small">Negation smoothing pulls toward neutral</div>
        <button onclick="useExample(&quot;I'm not that sad today 😊&quot;)">Use</button>
      </li>
      <li>
        <code>I am so sad 😁</code>
        <div class="small">Happy emoji + sad text conflict → Neutral</div>
        <button onclick="useExample('I am so sad 😁')">Use</button>
      </li>
      <li>
        <code>Feeling devastated and heartbroken 😭</code>
        <div class="small">Clearly sad → Negative</div>
        <button onclick="useExample('Feeling devastated and heartbroken 😭')">Use</button>
      </li>
    </ul>
  </div>
</body>
</html>
"""


def run_cli_sentiment(text: str, gif_url: str = ""):
  """Run sentiment analysis directly (no subprocess) for speed and reliability."""
  global MODELS_LOADED, IMAGE_MODEL, TEXT_MODEL

  # Load models once on first call
  if not MODELS_LOADED:
    try:
      print("Loading sentiment models... (this may take 10-15 seconds on first request)")
      IMAGE_MODEL, TEXT_MODEL = load_models()
      MODELS_LOADED = True
      print("Models loaded successfully!")
    except Exception as e:
      print(f"Error loading models: {e}")
      import traceback
      traceback.print_exc()
      return {"score": 0.0, "label": "Neutral", "error": f"Model loading failed: {str(e)}"}

  # Prepare input
  full_text = text
  if gif_url and gif_url.strip():
    full_text = f"{text} <img>{gif_url}</img>"

  try:
    # Get detailed sentiment
    details = get_sentiments_with_components([full_text], IMAGE_MODEL, TEXT_MODEL)
    if details and len(details) > 0:
      d0 = details[0]
      score = d0.get('combined_score', 0.0)
      label = d0.get('label', 'Neutral')
      result = {
        "score": float(score) if score is not None else 0.0,
        "label": label,
        "text_sentiment": float(d0.get('text_score')) if d0.get('text_score') is not None else None,
        "emoji_sentiment": float(d0.get('emoji_score')) if d0.get('emoji_score') is not None else None,
        "image_sentiment": float(d0.get('image_score')) if d0.get('image_score') is not None else None
      }
      # Update history (keep last 10)
      try:
        from time import time
        HISTORY.insert(0, {"input": text, "label": label, "score": float(result["score"]), "ts": int(time())})
        if len(HISTORY) > 10:
          del HISTORY[10:]
      except Exception:
        pass
      return result
    else:
      return {"score": 0.0, "label": "Neutral"}
  except Exception as e:
    print(f"Error analyzing sentiment: {e}")
    import traceback
    traceback.print_exc()
    return {"score": 0.0, "label": "Neutral", "error": str(e)}


class Handler(BaseHTTPRequestHandler):
  def _set_headers(self, status=200, content_type='text/html; charset=utf-8'):
    self.send_response(status)
    self.send_header('Content-Type', content_type)
    self.send_header('Cache-Control', 'no-store')
    self.end_headers()

  def do_GET(self):
    parsed = urlparse(self.path)
    if parsed.path in ('/', '/index.html'):
      self._set_headers(200, 'text/html; charset=utf-8')
      self.wfile.write(HTML_PAGE.encode('utf-8'))
    elif parsed.path == '/api/history':
      try:
        self._set_headers(200, 'application/json; charset=utf-8')
        self.wfile.write(json.dumps(HISTORY).encode('utf-8'))
      except Exception as e:
        self._set_headers(500, 'application/json; charset=utf-8')
        self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    else:
      self._set_headers(404, 'text/plain; charset=utf-8')
      self.wfile.write(b'Not Found')

  def do_POST(self):
    parsed = urlparse(self.path)
    if parsed.path == '/api/analyze':
      content_length = int(self.headers.get('Content-Length', 0))
      raw = self.rfile.read(content_length) if content_length > 0 else b''
      try:
        # Parse input with better error handling
        if not raw:
          self._set_headers(400, 'application/json; charset=utf-8')
          self.wfile.write(json.dumps({"error": "Empty request body"}).encode('utf-8'))
          return
        
        payload = json.loads(raw.decode('utf-8', errors='replace'))
        text = payload.get('text', '')
        
        # Validate input
        if not text or not text.strip():
          self._set_headers(400, 'application/json; charset=utf-8')
          self.wfile.write(json.dumps({"error": "Text is required"}).encode('utf-8'))
          return
        
        # Limit input length to prevent timeout
        if len(text) > 5000:
          self._set_headers(400, 'application/json; charset=utf-8')
          self.wfile.write(json.dumps({"error": "Text too long (max 5000 characters)"}).encode('utf-8'))
          return
        
        # Run sentiment analysis
        result = run_cli_sentiment(text.strip())
        
        # Ensure all values are JSON-serializable
        clean_result = {
          "score": float(result.get("score", 0.0)) if result.get("score") is not None else 0.0,
          "label": str(result.get("label", "Neutral")),
          "text_sentiment": float(result.get("text_sentiment")) if result.get("text_sentiment") is not None else None,
          "emoji_sentiment": float(result.get("emoji_sentiment")) if result.get("emoji_sentiment") is not None else None,
          "image_sentiment": float(result.get("image_sentiment")) if result.get("image_sentiment") is not None else None
        }
        
        self._set_headers(200, 'application/json; charset=utf-8')
        self.wfile.write(json.dumps(clean_result, ensure_ascii=False).encode('utf-8'))
      except json.JSONDecodeError as e:
        self._set_headers(400, 'application/json; charset=utf-8')
        self.wfile.write(json.dumps({"error": f"Invalid JSON: {str(e)}"}).encode('utf-8'))
      except Exception as e:
        print(f"Error in POST handler: {e}")
        import traceback
        traceback.print_exc()
        self._set_headers(500, 'application/json; charset=utf-8')
        self.wfile.write(json.dumps({"error": f"Server error: {str(e)}"}).encode('utf-8'))
    else:
      self._set_headers(404, 'text/plain; charset=utf-8')
      self.wfile.write(b'Not Found')


def run(host='127.0.0.1', port=7860):
    httpd = HTTPServer((host, port), Handler)
    print(f"Serving on http://{host}:{port} (Ctrl+C to quit)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == '__main__':
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', '7860'))
    run(host, port)
