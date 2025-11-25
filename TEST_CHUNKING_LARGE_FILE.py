# -*- coding: utf-8 -*-
"""
Test du Chunking Service sur fichier volumineux réel
Fichier: fusion_globale_2025-11-20_10-14-43.txt
"""

import requests
import json
import time
import os

CHUNKING_SERVICE = "http://localhost:5009"
FLASK_APP = "http://localhost:5008"
TEST_FILE = r"G:\memobrik\deuxieme_cerveau\fusion_global\fusion_globale_2025-11-20_10-14-43.txt"

def check_services():
    """Vérifie que les services tournent"""
    print("\n=== VERIFICATION SERVICES ===")
    
    # Flask Main
    try:
        r = requests.get(f"{FLASK_APP}/categories", timeout=3)
        print(f"✅ Flask Main (5008): OK - {r.status_code}")
    except:
        print("❌ Flask Main (5008): DOWN")
        return False
    
    # Chunking Service
    try:
        r = requests.get(f"{CHUNKING_SERVICE}/health", timeout=3)
        print(f"✅ Chunking Service (5009): OK - {r.status_code}")
    except:
        print("❌ Chunking Service (5009): DOWN")
        print("\n[ACTION] Lancer: START_CHUNKING_SERVICE.bat")
        return False
    
    return True

def load_test_file():
    """Charge le fichier de test"""
    print(f"\n=== CHARGEMENT FICHIER ===")
    print(f"Fichier: {TEST_FILE}")
    
    if not os.path.exists(TEST_FILE):
        print(f"❌ Fichier non trouvé: {TEST_FILE}")
        return None
    
    with open(TEST_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    line_count = content.count('\n') + 1
    char_count = len(content)
    
    print(f"✅ Chargé: {line_count} lignes, {char_count:,} caractères")
    
    return content

def test_detection(content):
    """Test détection besoin chunking"""
    print("\n=== TEST DETECTION ===")
    
    r = requests.post(f"{CHUNKING_SERVICE}/detect", json={
        "content": content,
        "line_threshold": 200,
        "char_threshold": 50000
    })
    
    result = r.json()
    data = result['data']
    
    print(f"Lignes: {data['line_count']} (seuil: {data['line_threshold']})")
    print(f"Chars: {data['char_count']:,} (seuil: {data['char_threshold']:,})")
    print(f"Chunking requis: {'✅ OUI' if data['needs_chunking'] else '❌ NON'}")
    
    return data['needs_chunking']

def test_chunking_methods(content):
    """Test différentes méthodes de chunking"""
    print("\n=== TEST METHODES CHUNKING ===")
    
    methods = [
        ("semantic", {"max_size": 4000, "overlap": 200}),
        ("tokens", {"max_tokens": 512, "overlap_tokens": 128}),
        ("smart", {"max_tokens": 512, "overlap_tokens": 128})
    ]
    
    results = {}
    
    for method, params in methods:
        print(f"\n[{method.upper()}]")
        
        start = time.time()
        r = requests.post(f"{CHUNKING_SERVICE}/chunk", json={
            "content": content,
            "method": method,
            **params
        })
        duration = time.time() - start
        
        if r.status_code == 200:
            result = r.json()
            stats = result['data']['stats']
            chunks = result['data']['chunks']
            
            print(f"  ✅ {stats['total_chunks']} chunks créés en {duration:.2f}s")
            print(f"  📊 Total tokens: {stats['total_tokens']:,}")
            print(f"  📊 Avg tokens/chunk: {stats['avg_tokens_per_chunk']}")
            print(f"  📊 Boundaries: {stats['boundary_types']}")
            
            # Preview premier chunk
            if chunks:
                preview = chunks[0]['preview']
                print(f"  📝 Preview chunk 1: {preview[:80]}...")
            
            results[method] = {
                "chunks": stats['total_chunks'],
                "tokens": stats['total_tokens'],
                "duration": duration,
                "stats": stats
            }
        else:
            print(f"  ❌ Erreur: {r.status_code}")
            results[method] = None
    
    return results

def test_organize_large(content):
    """Test organisation complète avec AI"""
    print("\n=== TEST ORGANISATION AI (CHUNKING) ===")
    print("⚠️ Ce test appelle l'API Gemini - peut prendre plusieurs minutes")
    
    response = input("\nContinuer? (y/n): ")
    if response.lower() != 'y':
        print("Test AI skippé")
        return None
    
    print("\n[INFO] Envoi au chunking service...")
    start = time.time()
    
    try:
        r = requests.post(f"{CHUNKING_SERVICE}/organize_large", json={
            "content": content,
            "category_name": "Test Fusion Globale",
            "chunk_method": "smart"
        }, timeout=600)  # 10 min timeout
        
        duration = time.time() - start
        
        if r.status_code == 200:
            result = r.json()
            data = result['data']
            
            print(f"\n✅ Organisation terminée en {duration:.2f}s")
            print(f"📊 Chunks traités: {data['chunks_processed']}")
            print(f"📊 Stats: {data['stats']}")
            print(f"\n📝 Contenu organisé (preview):")
            print("=" * 60)
            print(data['organized_content'][:1000])
            print("=" * 60)
            print(f"... ({len(data['organized_content'])} caractères total)")
            
            # Sauvegarder résultat
            output_file = "TEST_CHUNKING_OUTPUT.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(data['organized_content'])
            
            print(f"\n✅ Résultat sauvegardé: {output_file}")
            
            return data
        else:
            print(f"❌ Erreur: {r.status_code}")
            print(r.text)
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - traitement trop long")
        return None
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

def test_via_flask_route(content):
    """Test via route Flask /ai/organize (avec auto-détection)"""
    print("\n=== TEST VIA FLASK ROUTE (AUTO-DETECTION) ===")
    
    # Sauvegarder temporairement le contenu
    temp_file = "temp_test_fusion.txt"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[INFO] Fichier temp créé: {temp_file}")
    print("[INFO] Appel route Flask /ai/organize...")
    
    try:
        r = requests.post(f"{FLASK_APP}/ai/organize", json={
            "fusion_file": f"../{temp_file}",
            "category_name": "Test Auto-Detection"
        }, timeout=600)
        
        if r.status_code == 200:
            result = r.json()
            data = result['data']
            
            if data.get('chunked'):
                print(f"✅ Auto-détection: CHUNKING utilisé")
                print(f"📊 Chunks: {data['chunks_processed']}")
                print(f"📊 Stats: {data.get('stats', {})}")
            else:
                print(f"⚠️ Auto-détection: Méthode normale utilisée")
            
            print(f"📝 Fichier sauvegardé: {data['path']}")
            
            return data
        else:
            print(f"❌ Erreur: {r.status_code}")
            print(r.text)
            return None
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None
    finally:
        # Nettoyer
        if os.path.exists(temp_file):
            os.remove(temp_file)

def main():
    print("=" * 70)
    print("TEST CHUNKING SERVICE - FICHIER VOLUMINEUX REEL")
    print("=" * 70)
    
    # 1. Vérifier services
    if not check_services():
        print("\n❌ Services non disponibles")
        return
    
    # 2. Charger fichier
    content = load_test_file()
    if not content:
        return
    
    # 3. Test détection
    needs_chunking = test_detection(content)
    
    if not needs_chunking:
        print("\n⚠️ Fichier ne nécessite pas chunking selon seuils")
        response = input("Continuer quand même? (y/n): ")
        if response.lower() != 'y':
            return
    
    # 4. Test méthodes chunking
    chunking_results = test_chunking_methods(content)
    
    # 5. Comparaison méthodes
    print("\n=== COMPARAISON METHODES ===")
    for method, result in chunking_results.items():
        if result:
            print(f"{method:10} | {result['chunks']:3} chunks | {result['tokens']:6,} tokens | {result['duration']:.2f}s")
    
    # 6. Test organisation AI (optionnel)
    print("\n" + "=" * 70)
    ai_result = test_organize_large(content)
    
    # 7. Test via Flask (optionnel)
    if ai_result:
        print("\n" + "=" * 70)
        response = input("\nTester via route Flask avec auto-détection? (y/n): ")
        if response.lower() == 'y':
            flask_result = test_via_flask_route(content)
    
    print("\n" + "=" * 70)
    print("TESTS TERMINES")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[STOP] Interruption utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
