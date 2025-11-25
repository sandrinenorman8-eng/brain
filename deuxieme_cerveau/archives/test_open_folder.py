#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier que open_folder utilise les bons chemins
"""
import requests
import json

def test_open_folder(category):
    """Teste l'endpoint open_folder pour une catégorie"""
    url = f"http://localhost:5008/open_folder/{category}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        print(f"\n📁 Test: {category}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            path = data.get('path', 'N/A')
            print(f"   ✅ Chemin retourné: {path}")
            
            # Vérifier que le chemin contient la structure hiérarchique attendue
            if category == "todo" and "priorité" in path:
                print(f"   ✅ Mapping hiérarchique respecté!")
            elif category == "memobrik" and "logiciels" in path:
                print(f"   ✅ Mapping hiérarchique respecté!")
            elif category == "association" and "buziness" in path:
                print(f"   ✅ Mapping hiérarchique respecté!")
            else:
                print(f"   ⚠️  Vérifier le mapping pour cette catégorie")
        else:
            print(f"   ❌ Erreur: {data.get('error', 'Unknown')}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")

def main():
    print("=" * 80)
    print("TEST DES CHEMINS OPEN_FOLDER")
    print("=" * 80)
    
    # Tester plusieurs catégories avec mapping hiérarchique
    test_categories = [
        "todo",           # Devrait être dans priorité/todo
        "memobrik",       # Devrait être dans logiciels/memobrik
        "association",    # Devrait être dans buziness/association
        "scénario",       # Devrait être dans cinema/scénario
        "motivation",     # Devrait être dans livres/motivation
    ]
    
    for category in test_categories:
        test_open_folder(category)
    
    print("\n" + "=" * 80)
    print("TEST TERMINÉ")
    print("=" * 80)

if __name__ == '__main__':
    main()
