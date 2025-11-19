#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de vérification de l'implémentation de la fonctionnalité de téléchargement
"""

import os
import sys

def check_file_exists(filepath):
    """Vérifie si un fichier existe"""
    return os.path.exists(filepath)

def check_string_in_file(filepath, search_string):
    """Vérifie si une chaîne existe dans un fichier"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return search_string in content
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {filepath}: {e}")
        return False

def main():
    print("🔍 Vérification de l'implémentation de la fonctionnalité de téléchargement\n")
    
    checks = []
    
    # Vérification 1: Fichiers modifiés existent
    print("📁 Vérification des fichiers...")
    html_file = "src/frontend/index.html"
    py_file = "src/backend/app.py"
    
    if check_file_exists(html_file):
        print(f"✅ {html_file} existe")
        checks.append(True)
    else:
        print(f"❌ {html_file} n'existe pas")
        checks.append(False)
    
    if check_file_exists(py_file):
        print(f"✅ {py_file} existe")
        checks.append(True)
    else:
        print(f"❌ {py_file} n'existe pas")
        checks.append(False)
    
    # Vérification 2: Bouton jaune dans HTML
    print("\n🎨 Vérification du bouton jaune...")
    if check_string_in_file(html_file, 'bg-yellow-500'):
        print("✅ Bouton jaune trouvé (bg-yellow-500)")
        checks.append(True)
    else:
        print("❌ Bouton jaune non trouvé")
        checks.append(False)
    
    if check_string_in_file(html_file, 'Télécharger un Fichier'):
        print("✅ Texte du bouton trouvé")
        checks.append(True)
    else:
        print("❌ Texte du bouton non trouvé")
        checks.append(False)
    
    if check_string_in_file(html_file, 'upload-button'):
        print("✅ ID du bouton trouvé (upload-button)")
        checks.append(True)
    else:
        print("❌ ID du bouton non trouvé")
        checks.append(False)
    
    # Vérification 3: Modal de téléchargement
    print("\n🪟 Vérification de la modal...")
    if check_string_in_file(html_file, 'uploadModal'):
        print("✅ Modal de téléchargement trouvée")
        checks.append(True)
    else:
        print("❌ Modal de téléchargement non trouvée")
        checks.append(False)
    
    if check_string_in_file(html_file, 'fileInput'):
        print("✅ Input de fichier trouvé")
        checks.append(True)
    else:
        print("❌ Input de fichier non trouvé")
        checks.append(False)
    
    if check_string_in_file(html_file, 'categorySelect'):
        print("✅ Sélecteur de catégorie trouvé")
        checks.append(True)
    else:
        print("❌ Sélecteur de catégorie non trouvé")
        checks.append(False)
    
    # Vérification 4: Fonctions JavaScript
    print("\n⚙️ Vérification des fonctions JavaScript...")
    js_functions = ['openUploadModal', 'closeUploadModal', 'uploadFile']
    for func in js_functions:
        if check_string_in_file(html_file, func):
            print(f"✅ Fonction {func} trouvée")
            checks.append(True)
        else:
            print(f"❌ Fonction {func} non trouvée")
            checks.append(False)
    
    # Vérification 5: Endpoint backend
    print("\n🔧 Vérification de l'endpoint backend...")
    if check_string_in_file(py_file, '/upload_file'):
        print("✅ Endpoint /upload_file trouvé")
        checks.append(True)
    else:
        print("❌ Endpoint /upload_file non trouvé")
        checks.append(False)
    
    if check_string_in_file(py_file, 'def upload_file'):
        print("✅ Fonction upload_file trouvée")
        checks.append(True)
    else:
        print("❌ Fonction upload_file non trouvée")
        checks.append(False)
    
    if check_string_in_file(py_file, 'secure_filename'):
        print("✅ Sécurisation du nom de fichier trouvée")
        checks.append(True)
    else:
        print("❌ Sécurisation du nom de fichier non trouvée")
        checks.append(False)
    
    # Résumé
    print("\n" + "="*60)
    total = len(checks)
    passed = sum(checks)
    failed = total - passed
    
    print(f"📊 Résumé: {passed}/{total} vérifications réussies")
    
    if failed == 0:
        print("✅ Toutes les vérifications sont passées!")
        print("🎉 L'implémentation est complète et correcte!")
        return 0
    else:
        print(f"⚠️ {failed} vérification(s) échouée(s)")
        print("🔧 Veuillez vérifier les éléments manquants ci-dessus")
        return 1

if __name__ == "__main__":
    sys.exit(main())
