# -*- coding: utf-8 -*-
"""
Test connexion entre Flask et Chunking Service
"""

import requests
import json

print("=" * 60)
print("TEST CONNEXION CHUNKING SERVICE")
print("=" * 60)

# Test 1: Health
print("\n[1/3] Test health...")
try:
    r = requests.get("http://localhost:5009/health", timeout=3)
    print(f"✅ Health: {r.status_code}")
    print(json.dumps(r.json(), indent=2))
except Exception as e:
    print(f"❌ Erreur: {e}")
    exit(1)

# Test 2: Detect
print("\n[2/3] Test detect...")
try:
    r = requests.post("http://localhost:5009/detect", json={
        "content": "test\n" * 300,
        "line_threshold": 200
    }, timeout=3)
    print(f"✅ Detect: {r.status_code}")
    result = r.json()
    print(f"Needs chunking: {result['data']['needs_chunking']}")
    print(f"Lines: {result['data']['line_count']}")
except Exception as e:
    print(f"❌ Erreur: {e}")
    exit(1)

# Test 3: Chunk simple
print("\n[3/3] Test chunk...")
try:
    content = "# Test\n\nCeci est un test.\n\n" * 100
    r = requests.post("http://localhost:5009/chunk", json={
        "content": content,
        "method": "smart",
        "max_tokens": 512,
        "overlap_tokens": 128
    }, timeout=10)
    print(f"✅ Chunk: {r.status_code}")
    result = r.json()
    print(f"Chunks créés: {result['data']['stats']['total_chunks']}")
    print(f"Total tokens: {result['data']['stats']['total_tokens']}")
except Exception as e:
    print(f"❌ Erreur: {e}")
    exit(1)

print("\n" + "=" * 60)
print("✅ TOUS LES TESTS PASSES")
print("=" * 60)
print("\nChunking service opérationnel et accessible depuis Flask")
