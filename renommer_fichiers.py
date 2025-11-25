#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour renommer les fichiers existants du format "notes_YYYY-MM-DD.txt"
vers le nouveau format "CATEGORIE_YYYY-MM-DD.txt"
"""

import os
import json
from pathlib import Path

def load_categories():
    """Charge les catégories depuis categories.json"""
    categories_file = "deuxieme_cerveau/categories.json"
    if os.path.exists(categories_file):
        with open(categories_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def rename_files():
    """Renomme tous les fichiers du format notes_ vers CATEGORIE_"""
    categories = load_categories()
    renamed_count = 0

    print("🔄 Renommage des fichiers existants...")
    print("=" * 50)

    for cat in categories:
        category_dir = f"deuxieme_cerveau/{cat['name']}"

        if not os.path.exists(category_dir):
            continue

        print(f"\n📁 Traitement de la catégorie: {cat['emoji']} {cat['name']}")

        for filename in os.listdir(category_dir):
            if filename.startswith('notes_') and filename.endswith('.txt'):
                # Ancien format: notes_2025-09-12.txt
                # Nouveau format: CATEGORIE_2025-09-12.txt
                date_part = filename.replace('notes_', '').replace('.txt', '')
                new_filename = f"{cat['name']}_{date_part}.txt"
                old_path = os.path.join(category_dir, filename)
                new_path = os.path.join(category_dir, new_filename)

                try:
                    os.rename(old_path, new_path)
                    print(f"  ✅ {filename} → {new_filename}")
                    renamed_count += 1
                except Exception as e:
                    print(f"  ❌ Erreur lors du renommage de {filename}: {e}")

    print("\n" + "=" * 50)
    print(f"🎉 Renommage terminé ! {renamed_count} fichier(s) renommé(s)")
    return renamed_count

if __name__ == "__main__":
    print("🧠 Renommage des fichiers du Deuxième Cerveau")
    print("Ce script va convertir tous les fichiers 'notes_*.txt' vers 'CATEGORIE_*.txt'")
    print()

    # Vérifier si on est dans le bon répertoire
    if not os.path.exists("deuxieme_cerveau"):
        print("❌ Erreur: Dossier 'deuxieme_cerveau' introuvable")
        print("💡 Assurez-vous d'être dans le répertoire racine du projet")
        exit(1)

    # Demander confirmation
    response = input("⚠️  Voulez-vous continuer ? (o/N): ").lower().strip()
    if response not in ['o', 'oui', 'yes', 'y']:
        print("❌ Opération annulée")
        exit(0)

    # Renommer les fichiers
    rename_files()

    print("\n💡 Les nouveaux fichiers sauvegardés utiliseront automatiquement le nouveau format")
    print("🔄 Vous pouvez relancer ce script si vous avez ajouté de nouveaux fichiers")
