#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Navigation rapide dans les sections
Usage: python quick_nav.py [numéro_section]
"""

import sys
import json
import os

# Fix encoding pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def show_menu():
    """Affiche le menu de navigation"""
    with open('tasks.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("\n🎯 NAVIGATION RAPIDE - Extension Chrome\n")
    print("=" * 60)
    
    for phase in data['phases']:
        print(f"\n📁 {phase}")
        
        # Trouver sections de cette phase
        phase_sections = []
        if phase == "Setup & Architecture":
            phase_sections = [s for s in data['sections'] if 1 <= int(s['num']) <= 8]
        elif phase == "Configuration Extension":
            phase_sections = [s for s in data['sections'] if 9 <= int(s['num']) <= 10]
        elif phase == "Installation Multi-Machines":
            phase_sections = [s for s in data['sections'] if 11 <= int(s['num']) <= 19]
        elif phase == "Edge Cases & Corrections":
            phase_sections = [s for s in data['sections'] if 20 <= int(s['num']) <= 30]
        elif phase == "Validation & Debugging":
            phase_sections = [s for s in data['sections'] if 31 <= int(s['num']) <= 36]
        elif phase == "Workflows & Pipelines":
            phase_sections = [s for s in data['sections'] if 37 <= int(s['num']) <= 40]
        elif phase == "Checklists":
            phase_sections = [s for s in data['sections'] if 41 <= int(s['num']) <= 46]
        elif phase == "Annexes & Exemples":
            phase_sections = [s for s in data['sections'] if 47 <= int(s['num']) <= 67]
        
        for section in phase_sections[:3]:  # Montrer 3 premiers
            print(f"   {section['num']:>2}. {section['title'][:50]}")
        
        if len(phase_sections) > 3:
            print(f"   ... et {len(phase_sections) - 3} autres")
    
    print("\n" + "=" * 60)
    print("\n💡 Usage:")
    print("   python quick_nav.py [numéro]  - Ouvrir section spécifique")
    print("   python quick_nav.py quick     - Voir Quick Start")
    print("   python quick_nav.py list      - Lister toutes les sections")
    print()

def show_section(num):
    """Affiche le contenu d'une section"""
    with open('tasks.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    section = next((s for s in data['sections'] if s['num'] == str(num)), None)
    
    if not section:
        print(f"❌ Section {num} introuvable")
        return
    
    filepath = os.path.join('docs_chrome_extension', section['file'])
    
    if not os.path.exists(filepath):
        print(f"❌ Fichier introuvable: {filepath}")
        return
    
    print(f"\n📄 Section {section['num']}: {section['title']}")
    print(f"📊 {section['size']}")
    print("=" * 60)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
    
    print("\n" + "=" * 60)

def show_quick_start():
    """Affiche les sections Quick Start"""
    priority = [4, 9, 10, 41, 42]
    
    print("\n🚀 QUICK START - Sections Prioritaires\n")
    print("=" * 60)
    
    with open('tasks.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for num in priority:
        section = next((s for s in data['sections'] if int(s['num']) == num), None)
        if section:
            print(f"\n{section['num']:>2}. {section['title']}")
            print(f"    📄 {section['file']}")
            print(f"    📊 {section['size']}")
    
    print("\n" + "=" * 60)
    print("\n💡 Pour lire une section: python quick_nav.py [numéro]")
    print()

def list_all():
    """Liste toutes les sections"""
    with open('tasks.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n📋 TOUTES LES SECTIONS ({data['total_tasks']} total)\n")
    print("=" * 60)
    
    for section in data['sections']:
        print(f"{section['num']:>2}. {section['title'][:55]:<55} ({section['size'].split(',')[0]})")
    
    print("\n" + "=" * 60)
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_menu()
    elif sys.argv[1] == "quick":
        show_quick_start()
    elif sys.argv[1] == "list":
        list_all()
    else:
        try:
            num = int(sys.argv[1])
            show_section(num)
        except ValueError:
            print(f"❌ Numéro invalide: {sys.argv[1]}")
            show_menu()
