#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Quick test script for the server API"""
import json
try:
    import urllib.request as urlreq
except ImportError:
    import urllib2 as urlreq

def test_api(text):
    url = "http://127.0.0.1:7860/api/analyze"
    data = json.dumps({"text": text}).encode('utf-8')
    req = urlreq.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        response = urlreq.urlopen(req, timeout=30)
        result = json.loads(response.read().decode('utf-8'))
        print(f"\nInput: {text}")
        print(f"Score: {result.get('score')}")
        print(f"Label: {result.get('label')}")
        print(f"Text sentiment: {result.get('text_sentiment')}")
        print(f"Emoji sentiment: {result.get('emoji_sentiment')}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Testing server API...")
    test_api("am happy today")
    test_api("am happy today 😊")
    test_api("I am so sad 😢")
    test_api("I'm not that sad today 😊")
