# -*- coding: utf-8 -*-
"""
Test automatique Fusion IA avec MCP Playwright
Simule le clic sur "Organiser" et capture les logs
"""

import requests
import json
import time

FLASK_URL = "http://localhost:5008"
CHUNKING_URL = "http://localhost:5009"

print("=" * 70)
print("TEST AUTOMATIQUE FUSION IA")
print("=" * 70)

# 1. Vérifier services
print("\n[1/5] Vérification services...")
try:
    r = requests.get(f"{FLASK_URL}/categories", timeout=3)
    print(f"✅ Flask: {r.status_code}")
except:
    print("❌ Flask DOWN - Lancer: python deuxieme_cerveau/app_new.py")
    exit(1)

try:
    r = requests.get(f"{CHUNKING_URL}/health", timeout=3)
    print(f"✅ Chunking: {r.status_code}")
except:
    print("❌ Chunking DOWN - Lancer: python deuxieme_cerveau/chunking_service.py")
    exit(1)

# 2. Lister fusions disponibles
print("\n[2/5] Liste des fusions...")
r = requests.get(f"{FLASK_URL}/ai/list_fusions")
fusions = r.json()['data']['fusions']
print(f"✅ {len(fusions)} fusions trouvées")

if not fusions:
    print("❌ Aucune fusion disponible")
    exit(1)

# Prendre la fusion globale
fusion = next((f for f in fusions if f['type'] == 'global'), fusions[0])
print(f"📁 Fusion sélectionnée: {fusion['display_name']}")
print(f"📄 Fichier: {fusion['path']}")

# 3. Simuler le clic "Organiser"
print("\n[3/5] Simulation clic 'Organiser'...")
print(f"[INFO] Envoi requête POST /ai/organize")
print(f"[INFO] Fichier: {fusion['path']}")

start = time.time()

try:
    r = requests.post(f"{FLASK_URL}/ai/organize", json={
        "fusion_file": fusion['path'],
        "category_name": "Test Auto"
    }, timeout=600)
    
    duration = time.time() - start
    
    print(f"\n[4/5] Réponse reçue en {duration:.2f}s")
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        result = r.json()
        data = result['data']
        
        print(f"\n✅ SUCCÈS")
        print(f"Message: {result['message']}")
        
        if data.get('chunked'):
            print(f"\n📊 CHUNKING UTILISÉ:")
            print(f"   Chunks traités: {data['chunks_processed']}")
            print(f"   Stats: {data.get('stats', {})}")
        else:
            print(f"\n⚠️ Méthode normale utilisée (pas de chunking)")
        
        print(f"\n📝 Fichier sauvegardé: {data['path']}")
        print(f"📏 Taille contenu: {len(data['organized_content']):,} caractères")
        
        # Preview
        print(f"\n📄 PREVIEW (500 premiers caractères):")
        print("=" * 70)
        print(data['organized_content'][:500])
        print("=" * 70)
        
    else:
        print(f"\n❌ ERREUR {r.status_code}")
        print(r.text)
        
except requests.exceptions.Timeout:
    print(f"\n❌ TIMEOUT après {time.time() - start:.2f}s")
except Exception as e:
    print(f"\n❌ ERREUR: {e}")

print("\n[5/5] Vérification logs chunking service...")
print("\n⚠️ REGARDE LE TERMINAL DU CHUNKING SERVICE")
print("Tu devrais voir:")
print("  127.0.0.1 - - [DATE] \"POST /organize_large HTTP/1.1\" 200 -")
print("\nSi tu ne vois RIEN → Flask n'a pas redirigé vers chunking service")

print("\n" + "=" * 70)
print("TEST TERMINÉ")
print("=" * 70)
