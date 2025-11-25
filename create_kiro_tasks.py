#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Générateur de tasks.md pour Kiro
Crée un fichier de tâches interactif avec liens vers sections
"""

import os
import json
from pathlib import Path

def create_kiro_tasks(docs_dir="docs_chrome_extension", output_file="tasks.md"):
    """Génère tasks.md formaté pour Kiro"""
    
    # Lire l'index pour récupérer les sections
    index_path = os.path.join(docs_dir, "00_INDEX.md")
    
    if not os.path.exists(index_path):
        print(f"❌ Index introuvable: {index_path}")
        return
    
    # Parser l'index
    sections = []
    with open(index_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        current_section = None
        for line in lines:
            # Détecter titre de section: ## 1. Titre
            if line.startswith('## '):
                parts = line.strip().replace('## ', '').split('. ', 1)
                if len(parts) == 2:
                    num = parts[0]
                    title = parts[1]
                    current_section = {'num': num, 'title': title}
            
            # Détecter fichier: - **Fichier:** `filename.md`
            elif current_section and '**Fichier:**' in line:
                filename = line.split('`')[1] if '`' in line else ''
                current_section['file'] = filename
            
            # Détecter taille: - **Taille:** X lignes, Y caractères
            elif current_section and '**Taille:**' in line:
                size_info = line.split('**Taille:**')[1].strip()
                current_section['size'] = size_info
                sections.append(current_section)
                current_section = None
    
    # Créer tasks.md
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 🎯 Extension Chrome - Plan d'Action\n\n")
        f.write("> Guide complet de déploiement découpé en tâches actionnables\n\n")
        f.write("---\n\n")
        
        # Organiser par phases
        phases = {
            'Setup & Architecture': range(1, 9),
            'Configuration Extension': range(9, 11),
            'Installation Multi-Machines': range(11, 20),
            'Edge Cases & Corrections': range(20, 31),
            'Validation & Debugging': range(31, 37),
            'Workflows & Pipelines': range(37, 41),
            'Checklists': range(41, 47),
            'Annexes & Exemples': range(47, 68)
        }
        
        for phase_name, phase_range in phases.items():
            f.write(f"## {phase_name}\n\n")
            
            for section in sections:
                num = int(section['num'])
                if num in phase_range:
                    title = section['title']
                    filename = section['file']
                    size = section['size']
                    
                    # Format Kiro: - [ ] Titre → [Lien](fichier)
                    f.write(f"- [ ] **{title}**\n")
                    f.write(f"  - 📄 [{filename}]({docs_dir}/{filename})\n")
                    f.write(f"  - 📊 {size}\n\n")
            
            f.write("\n")
        
        # Section Quick Start
        f.write("---\n\n")
        f.write("## 🚀 Quick Start (Priorités)\n\n")
        f.write("Si tu veux démarrer rapidement, commence par ces sections :\n\n")
        
        priority_sections = [
            (4, "Architecture Globale"),
            (9, "Configuration Extension Chrome"),
            (10, "Sécurisation & Authentification"),
            (41, "Checklist Finale"),
            (42, "Extension Checklist")
        ]
        
        for num, title in priority_sections:
            matching = [s for s in sections if int(s['num']) == num]
            if matching:
                section = matching[0]
                f.write(f"- [ ] **{section['title']}**\n")
                f.write(f"  - [{section['file']}]({docs_dir}/{section['file']})\n\n")
        
        # Métadonnées
        f.write("\n---\n\n")
        f.write("## 📈 Progression\n\n")
        f.write(f"- **Total tâches:** {len(sections)}\n")
        f.write(f"- **Dossier docs:** `{docs_dir}/`\n")
        f.write(f"- **Index complet:** [{docs_dir}/00_INDEX.md]({docs_dir}/00_INDEX.md)\n\n")
        
        # Instructions
        f.write("## 💡 Comment utiliser\n\n")
        f.write("1. Coche les cases `[ ]` au fur et à mesure\n")
        f.write("2. Clique sur les liens pour ouvrir chaque section\n")
        f.write("3. Utilise Kiro pour exécuter les commandes des sections\n")
        f.write("4. Commence par le Quick Start si tu es pressé\n\n")
    
    print(f"✅ Fichier créé: {output_file}")
    print(f"   {len(sections)} tâches organisées en {len(phases)} phases")
    
    # Créer aussi un JSON pour automatisation
    json_file = output_file.replace('.md', '.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_tasks': len(sections),
            'phases': list(phases.keys()),
            'sections': sections
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Métadonnées: {json_file}")


if __name__ == "__main__":
    import sys
    
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs_chrome_extension"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "tasks.md"
    
    create_kiro_tasks(docs_dir, output_file)
