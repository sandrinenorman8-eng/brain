#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Met à jour la progression dans tasks.md
Usage: python update_progress.py [numéro_tâche]
"""

import sys
import re

# Fix encoding pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def count_completed(tasks_file='tasks.md'):
    """Compte les tâches complétées"""
    with open(tasks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    total = len(re.findall(r'- \[[ x]\]', content))
    completed = len(re.findall(r'- \[x\]', content))
    
    return completed, total

def mark_completed(task_num, tasks_file='tasks.md'):
    """Marque une tâche comme complétée"""
    with open(tasks_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Chercher la tâche
    task_pattern = rf'- \[ \] \*\*.*{task_num}.*\*\*'
    found = False
    
    for i, line in enumerate(lines):
        if re.search(task_pattern, line):
            lines[i] = line.replace('- [ ]', '- [x]')
            found = True
            break
    
    if found:
        with open(tasks_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        completed, total = count_completed(tasks_file)
        percentage = (completed / total * 100) if total > 0 else 0
        
        print(f"✅ Tâche {task_num} marquée comme complétée")
        print(f"📊 Progression: {completed}/{total} ({percentage:.1f}%)")
        
        # Barre de progression
        bar_length = 40
        filled = int(bar_length * completed / total)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"   [{bar}]")
    else:
        print(f"❌ Tâche {task_num} introuvable")

def show_progress(tasks_file='tasks.md'):
    """Affiche la progression actuelle"""
    completed, total = count_completed(tasks_file)
    percentage = (completed / total * 100) if total > 0 else 0
    
    print(f"\n📊 PROGRESSION GLOBALE\n")
    print("=" * 60)
    print(f"Complétées: {completed}/{total} ({percentage:.1f}%)")
    
    # Barre de progression
    bar_length = 50
    filled = int(bar_length * completed / total)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"\n[{bar}]\n")
    
    # Progression par phase
    with open(tasks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    phases = [
        "Setup & Architecture",
        "Configuration Extension",
        "Installation Multi-Machines",
        "Edge Cases & Corrections",
        "Validation & Debugging",
        "Workflows & Pipelines",
        "Checklists",
        "Annexes & Exemples"
    ]
    
    print("Détail par phase:")
    print("-" * 60)
    
    for phase in phases:
        # Extraire section de la phase
        phase_match = re.search(rf'## {re.escape(phase)}(.*?)(?=##|\Z)', content, re.DOTALL)
        if phase_match:
            phase_content = phase_match.group(1)
            phase_total = len(re.findall(r'- \[[ x]\]', phase_content))
            phase_completed = len(re.findall(r'- \[x\]', phase_content))
            phase_pct = (phase_completed / phase_total * 100) if phase_total > 0 else 0
            
            status = "✅" if phase_completed == phase_total else "🔄"
            print(f"{status} {phase:<35} {phase_completed:>2}/{phase_total:<2} ({phase_pct:>5.1f}%)")
    
    print("=" * 60)
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_progress()
    elif sys.argv[1] == "show":
        show_progress()
    else:
        try:
            task_num = int(sys.argv[1])
            mark_completed(task_num)
        except ValueError:
            print(f"❌ Numéro invalide: {sys.argv[1]}")
            print("\nUsage:")
            print("  python update_progress.py [numéro]  - Marquer tâche complétée")
            print("  python update_progress.py show      - Voir progression")
