#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier et corriger les incohérences entre categories.json et category_mapping.json
"""
import json
import os

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    # Charger les fichiers
    categories = load_json('categories.json')
    mapping = load_json('category_mapping.json')
    
    print("=" * 80)
    print("VÉRIFICATION DES MAPPINGS")
    print("=" * 80)
    
    # Extraire les noms de catégories
    category_names = {cat['name'] for cat in categories}
    mapping_keys = set(mapping.keys())
    
    print(f"\n📊 Statistiques:")
    print(f"   - Catégories dans categories.json: {len(category_names)}")
    print(f"   - Entrées dans category_mapping.json: {len(mapping_keys)}")
    
    # Catégories sans mapping
    print(f"\n❌ Catégories SANS mapping:")
    missing_mapping = category_names - mapping_keys
    for cat in sorted(missing_mapping):
        print(f"   - '{cat}'")
        # Proposer un mapping par défaut
        mapping[cat] = cat
    
    # Mappings sans catégorie
    print(f"\n⚠️  Mappings SANS catégorie correspondante:")
    orphan_mappings = mapping_keys - category_names
    for key in sorted(orphan_mappings):
        print(f"   - '{key}' -> '{mapping[key]}'")
    
    # Vérifier les dossiers existants
    print(f"\n📁 Vérification des dossiers physiques:")
    data_dir = 'data'
    
    for cat_name in category_names:
        mapped_path = mapping.get(cat_name, cat_name)
        full_path = os.path.join(data_dir, mapped_path)
        
        if os.path.exists(full_path):
            file_count = len([f for f in os.listdir(full_path) if f.endswith('.txt')])
            print(f"   ✅ {cat_name:30} -> {mapped_path:40} ({file_count} fichiers)")
        else:
            print(f"   ❌ {cat_name:30} -> {mapped_path:40} (DOSSIER MANQUANT)")
    
    # Sauvegarder le mapping corrigé
    if missing_mapping:
        print(f"\n💾 Sauvegarde du mapping corrigé...")
        save_json('category_mapping.json', mapping)
        print(f"   ✅ {len(missing_mapping)} entrées ajoutées")
    
    print("\n" + "=" * 80)
    print("VÉRIFICATION TERMINÉE")
    print("=" * 80)

if __name__ == '__main__':
    main()
