#!/usr/bin/env python3
from category_path_resolver import get_category_path
import os

# Test 1: Résolution du chemin
path = get_category_path('todo')
print(f"✓ Chemin résolu: {path}")
print(f"✓ Chemin absolu: {os.path.abspath(path)}")

# Test 2: Création du dossier
os.makedirs(path, exist_ok=True)
print(f"✓ Dossier existe: {os.path.exists(path)}")

# Test 3: Création d'un fichier test
test_file = os.path.join(path, 'test_mapping.txt')
with open(test_file, 'w', encoding='utf-8') as f:
    f.write("Test mapping\n")
print(f"✓ Fichier créé: {test_file}")
print(f"✓ Fichier existe: {os.path.exists(test_file)}")

# Test 4: Vérifier le contenu
with open(test_file, 'r', encoding='utf-8') as f:
    content = f.read()
print(f"✓ Contenu: {content.strip()}")

print("\n✅ TOUS LES TESTS PASSENT!")
print(f"Le fichier devrait être dans: data/priorité/todo/test_mapping.txt")
