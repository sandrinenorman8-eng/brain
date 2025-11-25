# -*- coding: utf-8 -*-
"""
Test DIRECT du chunking service sur fichier réel
Sans passer par Flask - test pur du service
"""

import requests
import time
import os

CHUNKING_URL = "http://localhost:5009"
TEST_FILE = r"G:\memobrik\deuxieme_cerveau\fusion_global\fusion_globale_2025-11-20_10-14-43.txt"

print("=" * 70)
print("TEST DIRECT CHUNKING SERVICE")
print("=" * 70)

# 1. Health check
print("\n[1/4] Health check...")
try:
    r = requests.get(f"{CHUNKING_URL}/health", timeout=3)
    if r.status_code == 200:
        print(f"✅ Service OK: {r.json()}")
    else:
        print(f"❌ Service erreur: {r.status_code}")
        exit(1)
except Exception as e:
    print(f"❌ Service DOWN: {e}")
    print("\n[ACTION] Lancer: cd deuxieme_cerveau && python chunking_service.py")
    exit(1)

# 2. Charger fichier
print("\n[2/4] Chargement fichier...")
if not os.path.exists(TEST_FILE):
    print(f"❌ Fichier non trouvé: {TEST_FILE}")
    exit(1)

with open(TEST_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.count('\n') + 1
chars = len(content)
print(f"✅ Chargé: {lines:,} lignes, {chars:,} caractères")

# 3. Test chunking smart
print("\n[3/4] Chunking smart (512 tokens, overlap 128)...")
start = time.time()

r = requests.post(f"{CHUNKING_URL}/chunk", json={
    "content": content,
    "method": "smart",
    "max_tokens": 512,
    "overlap_tokens": 128
})

duration = time.time() - start

if r.status_code == 200:
    result = r.json()
    stats = result['data']['stats']
    chunks = result['data']['chunks']
    
    print(f"✅ Chunking terminé en {duration:.2f}s")
    print(f"\n📊 STATISTIQUES:")
    print(f"   Chunks créés:      {stats['total_chunks']}")
    print(f"   Total tokens:      {stats['total_tokens']:,}")
    print(f"   Avg tokens/chunk:  {stats['avg_tokens_per_chunk']}")
    print(f"   Total chars:       {stats['total_chars']:,}")
    print(f"   Avg chars/chunk:   {stats['avg_chars_per_chunk']}")
    
    print(f"\n📝 PREVIEW CHUNKS:")
    for i, chunk in enumerate(chunks[:3]):  # 3 premiers
        print(f"\n   Chunk {i+1}:")
        print(f"   - Tokens: {chunk['token_count']}")
        print(f"   - Chars: {chunk['char_count']}")
        print(f"   - Boundary: {chunk['boundary_type']}")
        print(f"   - Preview: {chunk['preview'][:80]}...")
    
    if len(chunks) > 3:
        print(f"\n   ... et {len(chunks) - 3} autres chunks")
    
    # 4. Test organisation AI (optionnel)
    print("\n" + "=" * 70)
    print("[4/4] Test organisation AI avec Gemini")
    print("⚠️ Ceci va appeler l'API Gemini - peut prendre 10-20 minutes")
    print(f"⚠️ Environ {stats['total_chunks']} appels API seront effectués")
    
    response = input("\nContinuer? (y/n): ")
    
    if response.lower() == 'y':
        print("\n[INFO] Envoi au service pour organisation AI...")
        start_ai = time.time()
        
        try:
            r_ai = requests.post(f"{CHUNKING_URL}/organize_large", json={
                "content": content,
                "category_name": "Fusion Globale Test",
                "chunk_method": "smart"
            }, timeout=1200)  # 20 min timeout
            
            duration_ai = time.time() - start_ai
            
            if r_ai.status_code == 200:
                result_ai = r_ai.json()
                data = result_ai['data']
                
                print(f"\n✅ Organisation terminée en {duration_ai/60:.1f} minutes")
                print(f"\n📊 RESULTATS:")
                print(f"   Chunks traités: {data['chunks_processed']}")
                print(f"   Contenu final:  {len(data['organized_content']):,} caractères")
                
                # Sauvegarder
                output_file = "TEST_CHUNKING_OUTPUT.md"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(data['organized_content'])
                
                print(f"\n✅ Résultat sauvegardé: {output_file}")
                print(f"\n📝 PREVIEW (500 premiers caractères):")
                print("=" * 70)
                print(data['organized_content'][:500])
                print("=" * 70)
                
            else:
                print(f"❌ Erreur organisation: {r_ai.status_code}")
                print(r_ai.text)
                
        except requests.exceptions.Timeout:
            print("❌ Timeout - traitement trop long (>20 min)")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    else:
        print("\n[INFO] Test AI skippé")
    
else:
    print(f"❌ Erreur chunking: {r.status_code}")
    print(r.text)

print("\n" + "=" * 70)
print("TEST TERMINE")
print("=" * 70)
