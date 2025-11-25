# -*- coding: utf-8 -*-
"""
Test rapide du Chunking Service
"""

import requests
import json

BASE_URL = "http://localhost:5009"

def test_health():
    """Test health check"""
    print("\n=== TEST HEALTH ===")
    r = requests.get(f"{BASE_URL}/health")
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2))

def test_status():
    """Test status détaillé"""
    print("\n=== TEST STATUS ===")
    r = requests.get(f"{BASE_URL}/status")
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2))

def test_detect():
    """Test détection chunking"""
    print("\n=== TEST DETECT ===")
    
    # Petit fichier
    small_content = "Test\n" * 50
    r = requests.post(f"{BASE_URL}/detect", json={"content": small_content})
    print(f"Petit fichier (50 lignes): {r.json()['data']['needs_chunking']}")
    
    # Gros fichier
    large_content = "Test\n" * 300
    r = requests.post(f"{BASE_URL}/detect", json={"content": large_content})
    print(f"Gros fichier (300 lignes): {r.json()['data']['needs_chunking']}")

def test_chunk():
    """Test chunking"""
    print("\n=== TEST CHUNK ===")
    
    content = """
# Projet 1
Ceci est un projet important.
Il contient plusieurs idées.

## Détails
- Idée 1
- Idée 2
- Idée 3

# Projet 2
Un autre projet avec du contenu.
Plus de détails ici.
    """ * 20  # Répéter pour avoir du contenu
    
    r = requests.post(f"{BASE_URL}/chunk", json={
        "content": content,
        "method": "smart",
        "max_tokens": 512,
        "overlap_tokens": 128
    })
    
    result = r.json()
    print(f"Status: {r.status_code}")
    print(f"Chunks créés: {result['data']['stats']['total_chunks']}")
    print(f"Total tokens: {result['data']['stats']['total_tokens']}")
    print(f"Avg tokens/chunk: {result['data']['stats']['avg_tokens_per_chunk']}")

def test_organize_large():
    """Test organisation fichier volumineux"""
    print("\n=== TEST ORGANIZE LARGE ===")
    
    content = """
2025-11-20

Idée de projet: Application de gestion de tâches intelligente
- Utilise l'IA pour prioriser
- Intégration calendrier
- Notifications smart

Détails techniques:
- Backend Flask
- Frontend React
- Base de données PostgreSQL

Actions:
- Créer maquettes
- Définir API
- Commencer développement
    """ * 50  # Répéter pour simuler gros fichier
    
    r = requests.post(f"{BASE_URL}/organize_large", json={
        "content": content,
        "category_name": "Test Logiciels",
        "chunk_method": "smart"
    })
    
    result = r.json()
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print(f"Chunks traités: {result['data']['chunks_processed']}")
        print(f"Contenu organisé (preview):")
        print(result['data']['organized_content'][:500] + "...")
    else:
        print(f"Erreur: {result}")

if __name__ == "__main__":
    try:
        print("=" * 50)
        print("TEST CHUNKING SERVICE")
        print("=" * 50)
        
        test_health()
        test_status()
        test_detect()
        test_chunk()
        # test_organize_large()  # Décommenter si AI service configuré
        
        print("\n" + "=" * 50)
        print("TESTS TERMINES")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("\n[ERREUR] Service non disponible sur port 5009")
        print("Lancer: START_CHUNKING_SERVICE.bat")
    except Exception as e:
        print(f"\n[ERREUR] {e}")
