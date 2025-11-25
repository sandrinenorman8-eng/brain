#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Détecte les fichiers RÉELLEMENT utilisés par les processus actifs
"""
import psutil
import os
from pathlib import Path

def find_process_files(process_name_filter):
    """Trouve tous les fichiers ouverts par un processus"""
    active_files = set()
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Chercher les processus Python et Node
            if process_name_filter.lower() in proc.info['name'].lower():
                print(f"\n🔍 Processus trouvé: {proc.info['name']} (PID: {proc.info['pid']})")
                print(f"   Commande: {' '.join(proc.info['cmdline'] or [])}")
                
                # Récupérer les fichiers ouverts
                try:
                    open_files = proc.open_files()
                    for f in open_files:
                        file_path = f.path
                        # Filtrer uniquement les fichiers du projet
                        if 'deuxieme_cerveau' in file_path or 'memobrik' in file_path:
                            active_files.add(file_path)
                            print(f"   📄 {os.path.basename(file_path)}")
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    print(f"   ⚠️ Accès refusé aux fichiers ouverts")
                    
                # Analyser la ligne de commande pour trouver les fichiers
                cmdline = proc.info['cmdline'] or []
                for arg in cmdline:
                    if arg.endswith(('.py', '.js', '.html', '.json', '.bat')):
                        full_path = os.path.abspath(arg) if not os.path.isabs(arg) else arg
                        active_files.add(full_path)
                        print(f"   📌 Argument: {os.path.basename(arg)}")
                        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return active_files

def analyze_imports(file_path):
    """Analyse les imports d'un fichier Python ou JS"""
    imported_files = set()
    
    if not os.path.exists(file_path):
        return imported_files
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # Python imports
            if file_path.endswith('.py'):
                import re
                # from X import Y
                matches = re.findall(r'from\s+(\S+)\s+import', content)
                for match in matches:
                    if not match.startswith('.') and '.' not in match:
                        imported_files.add(f"{match}.py")
                
                # import X
                matches = re.findall(r'^import\s+(\S+)', content, re.MULTILINE)
                for match in matches:
                    if '.' not in match:
                        imported_files.add(f"{match}.py")
            
            # JavaScript requires
            elif file_path.endswith('.js'):
                import re
                matches = re.findall(r'require\([\'"](.+?)[\'"]\)', content)
                for match in matches:
                    if match.startswith('.'):
                        imported_files.add(match.replace('./', ''))
                    elif not match.startswith('fs') and not match.startswith('http'):
                        imported_files.add(f"{match}.js")
            
            # HTML references
            elif file_path.endswith('.html'):
                import re
                # src="..." ou href="..."
                matches = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', content)
                for match in matches:
                    if not match.startswith('http') and not match.startswith('#'):
                        imported_files.add(match)
                        
    except Exception as e:
        print(f"   ⚠️ Erreur lecture {file_path}: {e}")
    
    return imported_files

def main():
    print("=" * 80)
    print("DÉTECTION DES FICHIERS ACTIFS - ANALYSE DES PROCESSUS")
    print("=" * 80)
    print()
    
    # Chercher les processus Python (Flask)
    print("🔎 RECHERCHE DES PROCESSUS PYTHON (Flask)...")
    python_files = find_process_files('python')
    
    # Chercher les processus Node (Search server)
    print("\n🔎 RECHERCHE DES PROCESSUS NODE.JS (Search)...")
    node_files = find_process_files('node')
    
    # Combiner tous les fichiers actifs
    all_active_files = python_files | node_files
    
    print("\n" + "=" * 80)
    print("📋 FICHIERS ACTIFS DÉTECTÉS")
    print("=" * 80)
    
    if not all_active_files:
        print("⚠️ Aucun fichier actif détecté!")
        print("   Les serveurs sont-ils démarrés?")
        print("   Lancez START.bat puis relancez ce script.")
    else:
        project_files = []
        for f in sorted(all_active_files):
            basename = os.path.basename(f)
            if any(ext in basename for ext in ['.py', '.js', '.html', '.json', '.bat']):
                project_files.append(basename)
                print(f"  ✓ {basename}")
        
        # Analyser les imports
        print("\n" + "=" * 80)
        print("📦 ANALYSE DES IMPORTS/DÉPENDANCES")
        print("=" * 80)
        
        imported_files = set()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        for filename in project_files:
            file_path = os.path.join(base_dir, filename)
            if os.path.exists(file_path):
                imports = analyze_imports(file_path)
                if imports:
                    print(f"\n📄 {filename} importe:")
                    for imp in sorted(imports):
                        print(f"   → {imp}")
                        imported_files.add(imp)
        
        # Liste finale des fichiers nécessaires
        print("\n" + "=" * 80)
        print("✅ FICHIERS NÉCESSAIRES (actifs + importés)")
        print("=" * 80)
        
        necessary_files = set(project_files) | imported_files
        for f in sorted(necessary_files):
            print(f"  ✓ {f}")
        
        # Comparer avec tous les fichiers du projet
        print("\n" + "=" * 80)
        print("🗑️ FICHIERS POTENTIELLEMENT INUTILISÉS")
        print("=" * 80)
        
        all_project_files = set()
        for f in os.listdir(base_dir):
            if f.endswith(('.py', '.js', '.html', '.json', '.bat', '.ps1')):
                all_project_files.add(f)
        
        unused_files = all_project_files - necessary_files
        
        if unused_files:
            for f in sorted(unused_files):
                file_path = os.path.join(base_dir, f)
                size = os.path.getsize(file_path) / 1024
                print(f"  ❌ {f:50} ({size:.1f} KB)")
        else:
            print("  ✓ Tous les fichiers sont utilisés!")
        
        print(f"\n📊 Total fichiers nécessaires: {len(necessary_files)}")
        print(f"📊 Total fichiers inutilisés: {len(unused_files)}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Analyse interrompue")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
