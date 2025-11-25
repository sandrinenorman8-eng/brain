#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Smart Document Splitter - Découpe intelligente de documents massifs
Détecte automatiquement les sections et crée des fichiers séparés
"""

import re
import os
from pathlib import Path

class SmartDocSplitter:
    def __init__(self, input_file, output_dir="docs_split"):
        self.input_file = input_file
        self.output_dir = output_dir
        self.sections = []
        
    def detect_sections(self):
        """Détecte les sections basées sur les patterns de titres"""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Patterns de détection (ordre de priorité)
        patterns = [
            (r'^#{1,3}\s+(\d+\.?\s+)?(.+?)(?:\s+\{#[\w-]+\})?$', 'markdown'),  # ## 1. TITRE {#id}
            (r'^[A-Z\s]{10,}$', 'uppercase'),  # TITRE EN MAJUSCULES
            (r'^(\d+\.)+\s+[A-Z]', 'numbered'),  # 1.1 Titre
            (r'^Phase\s+\d+\s*:', 'phase'),  # Phase 1:
        ]
        
        lines = content.split('\n')
        current_section = {'title': 'Introduction', 'start': 0, 'content': []}
        
        for i, line in enumerate(lines):
            is_title = False
            title_text = None
            
            for pattern, ptype in patterns:
                match = re.match(pattern, line.strip())
                if match:
                    is_title = True
                    if ptype == 'markdown':
                        title_text = match.group(2).strip()
                    elif ptype == 'uppercase':
                        title_text = line.strip()
                    elif ptype == 'numbered':
                        title_text = line.strip()
                    elif ptype == 'phase':
                        title_text = line.strip()
                    break
            
            if is_title and title_text and len(current_section['content']) > 5:
                # Sauvegarder section précédente
                current_section['end'] = i - 1
                self.sections.append(current_section)
                
                # Nouvelle section
                current_section = {
                    'title': self._clean_title(title_text),
                    'start': i,
                    'content': [line]
                }
            else:
                current_section['content'].append(line)
        
        # Dernière section
        current_section['end'] = len(lines) - 1
        self.sections.append(current_section)
        
        return len(self.sections)
    
    def _clean_title(self, title):
        """Nettoie le titre pour créer un nom de fichier valide"""
        # Enlever caractères spéciaux
        title = re.sub(r'[^\w\s-]', '', title)
        # Remplacer espaces par underscores
        title = re.sub(r'\s+', '_', title.strip())
        # Limiter longueur
        title = title[:60]
        return title.lower()
    
    def split_and_save(self):
        """Découpe et sauvegarde chaque section"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        manifest = []
        
        for idx, section in enumerate(self.sections, 1):
            filename = f"{idx:02d}_{section['title']}.md"
            filepath = os.path.join(self.output_dir, filename)
            
            # Écrire section
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(section['content']))
            
            # Stats
            lines_count = len(section['content'])
            chars_count = sum(len(line) for line in section['content'])
            
            manifest.append({
                'index': idx,
                'title': section['title'],
                'filename': filename,
                'lines': lines_count,
                'chars': chars_count
            })
            
            print(f"✅ {filename} ({lines_count} lignes, {chars_count} chars)")
        
        # Créer index
        self._create_index(manifest)
        
        return manifest
    
    def _create_index(self, manifest):
        """Crée un fichier index avec liens vers toutes les sections"""
        index_path = os.path.join(self.output_dir, "00_INDEX.md")
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("# 📚 Index du Document\n\n")
            f.write(f"**Document source:** {self.input_file}\n")
            f.write(f"**Sections détectées:** {len(manifest)}\n\n")
            f.write("---\n\n")
            
            for item in manifest:
                f.write(f"## {item['index']}. {item['title'].replace('_', ' ').title()}\n")
                f.write(f"- **Fichier:** `{item['filename']}`\n")
                f.write(f"- **Taille:** {item['lines']} lignes, {item['chars']:,} caractères\n\n")
        
        print(f"\n📋 Index créé: {index_path}")
    
    def get_summary(self):
        """Retourne un résumé des sections détectées"""
        total_lines = sum(len(s['content']) for s in self.sections)
        total_chars = sum(sum(len(line) for line in s['content']) for s in self.sections)
        
        return {
            'total_sections': len(self.sections),
            'total_lines': total_lines,
            'total_chars': total_chars,
            'sections': [{'title': s['title'], 'lines': len(s['content'])} for s in self.sections]
        }


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python smart_doc_splitter.py <fichier_input> [dossier_output]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "docs_split"
    
    if not os.path.exists(input_file):
        print(f"❌ Fichier introuvable: {input_file}")
        sys.exit(1)
    
    print(f"🔍 Analyse de: {input_file}")
    print(f"📁 Sortie vers: {output_dir}\n")
    
    splitter = SmartDocSplitter(input_file, output_dir)
    
    # Détection
    num_sections = splitter.detect_sections()
    print(f"✨ {num_sections} sections détectées\n")
    
    # Découpage
    print("📝 Création des fichiers...\n")
    manifest = splitter.split_and_save()
    
    # Résumé
    summary = splitter.get_summary()
    print(f"\n🎉 Terminé!")
    print(f"   Total: {summary['total_lines']:,} lignes, {summary['total_chars']:,} caractères")
    print(f"   Répartis en {summary['total_sections']} fichiers")


if __name__ == "__main__":
    main()
