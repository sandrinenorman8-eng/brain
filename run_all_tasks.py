#!/usr/bin/env python3
"""
Script pour lancer toutes les tâches de l'extension Chrome d'un coup
"""
import os
import sys

def read_all_sections():
    """Lit toutes les sections dans l'ordre"""
    docs_dir = "docs_chrome_extension"
    
    # Liste des fichiers dans l'ordre
    sections = []
    for i in range(1, 68):  # 67 sections
        files = [f for f in os.listdir(docs_dir) if f.startswith(f"{i:02d}_")]
        if files:
            sections.append(os.path.join(docs_dir, files[0]))
    
    return sections

def display_section(filepath):
    """Affiche une section"""
    print("\n" + "="*80)
    print(f"📄 {os.path.basename(filepath)}")
    print("="*80 + "\n")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f"❌ Erreur lecture: {e}")
    
    print("\n" + "-"*80)

def main():
    print("🚀 LANCEMENT DE TOUTES LES TÂCHES")
    print("="*80)
    
    sections = read_all_sections()
    total = len(sections)
    
    print(f"\n📊 {total} sections à traiter\n")
    
    mode = input("Mode:\n1. Tout afficher d'un coup\n2. Section par section (appuyer Entrée)\n3. Quick Start seulement\nChoix: ")
    
    if mode == "3":
        # Quick Start
        quick_sections = [4, 9, 10, 41, 42]
        sections = [s for i, s in enumerate(sections, 1) if i in quick_sections]
        print(f"\n🎯 Mode Quick Start: {len(sections)} sections prioritaires\n")
    
    for i, section in enumerate(sections, 1):
        display_section(section)
        
        if mode == "2":
            response = input(f"\n[{i}/{len(sections)}] Continuer? (Entrée=oui, q=quitter): ")
            if response.lower() == 'q':
                print("\n👋 Arrêt demandé")
                break
    
    print("\n✅ TERMINÉ!")
    print(f"📈 Sections traitées: {i}/{len(sections)}")

if __name__ == "__main__":
    main()
