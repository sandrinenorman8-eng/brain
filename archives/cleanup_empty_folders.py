#!/usr/bin/env python3
"""
Script pour nettoyer les dossiers vides créés par erreur à la racine de data/
Ces dossiers devraient être dans leurs dossiers parents respectifs selon folder_hierarchy.json
"""

import os
import shutil
import json

# Dossiers à supprimer (créés par erreur à la racine de data/)
FOLDERS_TO_REMOVE = [
    'association',
    'idée business',
    'la villa de la paix',
    'lagence',
    'money brick',
    'opportunité',
    'todo',  # Devrait être dans priorité/
    'extentions'  # Typo, devrait être supprimé
]

def check_folder_empty(folder_path):
    """Vérifie si un dossier est vide (pas de fichiers, seulement des sous-dossiers vides)"""
    if not os.path.exists(folder_path):
        return True
    
    for root, dirs, files in os.walk(folder_path):
        if files:  # Si on trouve des fichiers
            return False
    return True

def cleanup_empty_folders():
    """Supprime les dossiers vides de la liste"""
    data_dir = 'data'
    
    if not os.path.exists(data_dir):
        print(f"❌ Le dossier {data_dir} n'existe pas")
        return
    
    print("🔍 Vérification des dossiers à supprimer...")
    print("=" * 60)
    
    removed_count = 0
    skipped_count = 0
    
    for folder_name in FOLDERS_TO_REMOVE:
        folder_path = os.path.join(data_dir, folder_name)
        
        if not os.path.exists(folder_path):
            print(f"⏭️  {folder_name}: N'existe pas (déjà supprimé?)")
            continue
        
        # Vérifier si le dossier est vide
        if check_folder_empty(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"✅ {folder_name}: Supprimé (vide)")
                removed_count += 1
            except Exception as e:
                print(f"❌ {folder_name}: Erreur lors de la suppression - {e}")
                skipped_count += 1
        else:
            print(f"⚠️  {folder_name}: CONTIENT DES FICHIERS - NON SUPPRIMÉ")
            print(f"   Vérifiez manuellement ce dossier avant de le supprimer")
            skipped_count += 1
    
    print("=" * 60)
    print(f"📊 Résumé:")
    print(f"   ✅ Dossiers supprimés: {removed_count}")
    print(f"   ⏭️  Dossiers ignorés: {skipped_count}")
    
    # Vérifier la structure finale
    print("\n🔍 Structure finale de data/:")
    print("=" * 60)
    for item in sorted(os.listdir(data_dir)):
        item_path = os.path.join(data_dir, item)
        if os.path.isdir(item_path):
            # Compter les sous-dossiers
            subdirs = [d for d in os.listdir(item_path) if os.path.isdir(os.path.join(item_path, d))]
            files = [f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))]
            print(f"📁 {item}/")
            if subdirs:
                print(f"   └─ {len(subdirs)} sous-dossiers")
            if files:
                print(f"   └─ {len(files)} fichiers")

if __name__ == '__main__':
    print("🧹 NETTOYAGE DES DOSSIERS VIDES")
    print("=" * 60)
    print("Ce script va supprimer les dossiers vides créés par erreur")
    print("à la racine de data/")
    print()
    
    response = input("Continuer? (o/n): ").strip().lower()
    if response == 'o' or response == 'oui':
        cleanup_empty_folders()
        print("\n✅ Nettoyage terminé!")
    else:
        print("❌ Nettoyage annulé")
