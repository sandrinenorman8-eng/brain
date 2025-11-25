#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test direct de la route AI"""

import sys
sys.path.insert(0, 'deuxieme_cerveau')

from app_new import app, AI_AVAILABLE

print(f"AI_AVAILABLE: {AI_AVAILABLE}")
print("\nRoutes AI disponibles:")

with app.test_client() as client:
    # Test de la route /ai/test
    print("\n1. Test de /ai/test...")
    response = client.get('/ai/test')
    print(f"   Status: {response.status_code}")
    print(f"   Data: {response.get_json()}")
    
    # Test de la route /ai/list_fusions
    print("\n2. Test de /ai/list_fusions...")
    response = client.get('/ai/list_fusions')
    print(f"   Status: {response.status_code}")
    data = response.get_json()
    if data:
        print(f"   Fusions: {data.get('data', {}).get('fusions', [])}")
    
print("\n✅ Tests terminés")
