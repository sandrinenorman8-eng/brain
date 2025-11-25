#!/usr/bin/env python3
"""
Script pour générer automatiquement les données des fichiers
pour la version indépendante de all_notes.html
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

def scan_category_folders():
    """Scanne tous les dossiers de catégories et génère les données des fichiers"""
    
    # Charger les catégories depuis categories.json
    categories_file = Path('categories.json')
    if not categories_file.exists():
        print("❌ Fichier categories.json non trouvé")
        return {}
    
    with open(categories_file, 'r', encoding='utf-8') as f:
        categories = json.load(f)
    
    files_data = {}
    
    for category in categories:
        category_name = category['name']
        category_path = Path(category_name)
        
        if not category_path.exists() or not category_path.is_dir():
            print(f"⚠️  Dossier '{category_name}' non trouvé")
            continue
        
        files = []
        
        # Scanner tous les fichiers dans le dossier
        for file_path in category_path.iterdir():
            if file_path.is_file() and file_path.suffix in ['.txt', '.md', '.html']:
                # Extraire la date du nom de fichier si possible
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', file_path.name)
                
                if date_match:
                    file_date = date_match.group(1)
                else:
                    # Utiliser la date de modification du fichier
                    mod_time = file_path.stat().st_mtime
                    file_date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
                
                files.append({
                    'name': file_path.name,
                    'date': file_date,
                    'path': str(file_path)
                })
        
        if files:
            # Trier par date (plus récent en premier)
            files.sort(key=lambda x: x['date'], reverse=True)
            files_data[category_name] = files
            print(f"✅ {category_name}: {len(files)} fichiers trouvés")
        else:
            print(f"⚠️  {category_name}: aucun fichier trouvé")
    
    return files_data

def update_standalone_html(files_data):
    """Met à jour le fichier HTML standalone avec les nouvelles données"""
    
    html_file = Path('all_notes_standalone.html')
    if not html_file.exists():
        print("❌ Fichier all_notes_standalone.html non trouvé")
        return False
    
    # Lire le fichier HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Générer le JavaScript avec les nouvelles données
    js_data = json.dumps(files_data, indent=12, ensure_ascii=False)
    
    # Remplacer les données dans le fichier HTML
    pattern = r'const filesData = \{[^}]*\};'
    replacement = f'const filesData = {js_data};'
    
    # Chercher le pattern plus flexible
    pattern = r'const filesData = \{.*?\};'
    if not re.search(pattern, html_content, re.DOTALL):
        # Si le pattern n'est pas trouvé, chercher une version plus simple
        pattern = r'const filesData = \{[^}]*\}'
        if not re.search(pattern, html_content):
            print("❌ Impossible de trouver la section filesData dans le HTML")
            return False
    
    updated_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # Sauvegarder le fichier mis à jour
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ Fichier HTML mis à jour avec succès")
    return True

def main():
    """Fonction principale"""
    print("🚀 Génération des données pour all_notes_standalone.html")
    print("=" * 50)
    
    # Scanner les dossiers
    files_data = scan_category_folders()
    
    if not files_data:
        print("❌ Aucune donnée trouvée")
        return
    
    # Sauvegarder les données dans un fichier JSON pour référence
    with open('files_data.json', 'w', encoding='utf-8') as f:
        json.dump(files_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Données sauvegardées dans files_data.json")
    
    # Mettre à jour le fichier HTML
    if update_standalone_html(files_data):
        print("🎉 Mise à jour terminée avec succès!")
        print(f"📊 Total: {sum(len(files) for files in files_data.values())} fichiers dans {len(files_data)} catégories")
    else:
        print("❌ Erreur lors de la mise à jour du fichier HTML")

if __name__ == "__main__":
    main()
