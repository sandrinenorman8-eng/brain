#!/usr/bin/env python3
"""
Test de l'intégration Flask avec le système de recherche
"""

import requests
import json
import time

def test_flask_server():
    """Test du serveur Flask"""
    print("🧪 TEST DE L'INTÉGRATION FLASK")
    print("=" * 50)
    
    base_url = "http://localhost:5008"
    
    # Test 1: Page all_notes
    print("\n1️⃣ Test de la page /all_notes")
    try:
        response = requests.get(f"{base_url}/all_notes", timeout=10)
        if response.status_code == 200:
            print("✅ Page all_notes accessible")
            if "search" in response.text.lower():
                print("✅ Contenu de recherche détecté")
            else:
                print("⚠️ Contenu de recherche non détecté")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text[:200]}")
    except requests.exceptions.ConnectionError:
        print("❌ Serveur Flask non accessible sur le port 5008")
        print("💡 Démarrez le serveur avec: python app.py")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Test 2: API all_notes_data
    print("\n2️⃣ Test de l'API /all_notes_data")
    try:
        response = requests.get(f"{base_url}/all_notes_data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API all_notes_data fonctionne")
            print(f"📊 {data.get('categories_count', 0)} catégories, {data.get('total_files', 0)} fichiers")
        else:
            print(f"❌ Erreur API: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur API: {e}")
    
    # Test 3: API search_content
    print("\n3️⃣ Test de l'API /search_content")
    try:
        search_data = {"term": "dans"}
        response = requests.post(f"{base_url}/search_content", 
                               json=search_data, 
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results_count = len(data.get('results', []))
            print(f"✅ API search_content fonctionne")
            print(f"🔍 Recherche 'dans': {results_count} résultats")
            
            if results_count > 0:
                first_result = data['results'][0]
                print(f"📄 Premier résultat: {first_result.get('category')}/{first_result.get('filename')}")
        elif response.status_code == 503:
            print("⚠️ Serveur de recherche Node.js non disponible")
            print("💡 Démarrez-le avec: node search-server.js")
        else:
            print(f"❌ Erreur search: {response.status_code} - {response.text[:200]}")
    except Exception as e:
        print(f"❌ Erreur search: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test terminé")
    return True

def test_direct_access():
    """Test d'accès direct aux fichiers"""
    print("\n🔗 TEST D'ACCÈS DIRECT")
    print("-" * 30)
    
    # Test du fichier standalone
    try:
        with open('all_notes_standalone.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'performSearch' in content:
                print("✅ Fichier standalone contient les fonctions de recherche")
            else:
                print("❌ Fichier standalone manque les fonctions de recherche")
                
            if 'toggleAccordion' in content:
                print("✅ Fichier standalone contient les fonctions d'accordéon")
            else:
                print("❌ Fichier standalone manque les fonctions d'accordéon")
                
    except FileNotFoundError:
        print("❌ Fichier all_notes_standalone.html non trouvé")
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")

if __name__ == "__main__":
    print("🚀 Démarrage des tests d'intégration Flask...")
    print(f"📅 {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_flask_server()
    test_direct_access()
    
    print("\n💡 Pour tester manuellement:")
    print("1. Ouvrez http://localhost:5008/all_notes")
    print("2. Testez la recherche avec des mots comme 'dans', 'test', 'projet'")
    print("3. Vérifiez que les accordéons s'ouvrent/ferment correctement")
