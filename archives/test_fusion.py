#!/usr/bin/env python3
import requests
import json

# Test fusion category
print("Testing /fusion/category...")
response = requests.post(
    'http://localhost:5008/fusion/category',
    json={'categories': ['todo', 'memobrik']},
    headers={'Content-Type': 'application/json'}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()

# Test fusion global
print("Testing /fusion/global...")
response = requests.post(
    'http://localhost:5008/fusion/global',
    json={},
    headers={'Content-Type': 'application/json'}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
