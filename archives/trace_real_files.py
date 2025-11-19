#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trace les fichiers RÉELLEMENT utilisés en analysant:
1. Les processus actifs (app.py, search-server-fixed.js)
2. Les imports directs dans ces fichiers
3. Les fichiers référencés dans index.html
"""
import os
import re

# Fichiers de démarrage
ENTRY_POINTS = {
    'app.py': 'Flask application',
    'search-server-fixed.js': 'Node.js search server',
    'index.html': 'Main UI',
    'all_notes_standalone.html': 'Standalone notes viewer',
}

# Fichiers système nécessaires
SYSTEM_FILES = {
    'START.bat': 'Startup script',
    'STOP.bat': 'Shutdown script',
    'requirements.txt': 'Python dependencies',
    'package.json': 'Node.js metadata',
    'pyrightconfig.json': 'Python type checking',
    'categories.json': 'Category definitions',
    'category_mapping.json': 'Path mappings',
}

def analyze_python_imports(filepath):
    """Analyse les imports Python"""
    imports = set()
    
    if not os.path.exists(filepath):
        return imports
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # from X import Y
            matches = re.findall(r'from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import', content)
            for match in matches:
                # Ignorer les modules standard
                if match not in ['flask', 'datetime', 'os', 're', 'json', 'random', 'zipfile', 'shutil', 'functools', 'werkzeug', 'pathlib']:
                    imports.add(f"{match}.py")
            
            # import X
            matches = re.findall(r'^import\s+([a-zA-Z_][a-zA-Z0-9_]*)', content, re.MULTILINE)
            for match in matches:
                if match not in ['os', 're', 'json', 'random', 'zipfile', 'shutil', 'functools', 'datetime', 'pathlib']:
                    imports.add(f"{match}.py")
                    
    except Exception as e:
        print(f"⚠️ Erreur lecture {filepath}: {e}")
    
    return imports

def analyze_js_requires(filepath):
    """Analyse les requires JavaScript"""
    requires = set()
    
    if not os.path.exists(filepath):
        return requires
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # require('...')
            matches = re.findall(r'require\([\'"]([^\'"]+)[\'"]\)', content)
            for match in matches:
                # Ignorer les modules Node.js standard
                if match not in ['fs', 'path', 'http', 'url', 'https']:
                    if match.startswith('./'):
                        requires.add(match.replace('./', ''))
                    elif not match.startswith('fs') and not match.startswith('http'):
                        requires.add(match)
                        
    except Exception as e:
        print(f"⚠️ Erreur lecture {filepath}: {e}")
    
    return requires

def analyze_html_references(filepath):
    """Analyse les références dans HTML"""
    refs = set()
    
    if not os.path.exists(filepath):
        return refs
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # src="..." ou href="..."
            matches = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', content)
            for match in matches:
                # Ignorer les URLs externes et les ancres
                if not match.startswith('http') and not match.startswith('#') and not match.startswith('/'):
                    # Extraire juste le nom du fichier
                    filename = os.path.basename(match)
                    if filename and '.' in filename:
                        refs.add(filename)
                        
    except Exception as e:
        print(f"⚠️ Erreur lecture {filepath}: {e}")
    
    return refs

def main():
    print("=" * 80)
    print("TRAÇAGE DES FICHIERS RÉELLEMENT UTILISÉS")
    print("=" * 80)
    print()
    
    necessary_files = set()
    
    # 1. Ajouter les fichiers système
    print("📦 FICHIERS SYSTÈME NÉCESSAIRES:")
    for filename, desc in SYSTEM_FILES.items():
        print(f"  ✓ {filename:40} - {desc}")
        necessary_files.add(filename)
    
    # 2. Analyser les points d'entrée
    print("\n🔍 ANALYSE DES POINTS D'ENTRÉE:")
    
    to_analyze = list(ENTRY_POINTS.keys())
    analyzed = set()
    
    while to_analyze:
        current_file = to_analyze.pop(0)
        
        if current_file in analyzed:
            continue
        
        analyzed.add(current_file)
        necessary_files.add(current_file)
        
        print(f"\n  📄 {current_file}")
        
        # Analyser selon le type de fichier
        if current_file.endswith('.py'):
            imports = analyze_python_imports(current_file)
            for imp in imports:
                print(f"     → {imp}")
                if imp not in analyzed:
                    to_analyze.append(imp)
                necessary_files.add(imp)
        
        elif current_file.endswith('.js'):
            requires = analyze_js_requires(current_file)
            for req in requires:
                print(f"     → {req}")
                if req not in analyzed:
                    to_analyze.append(req)
                necessary_files.add(req)
        
        elif current_file.endswith('.html'):
            refs = analyze_html_references(current_file)
            for ref in refs:
                print(f"     → {ref}")
                necessary_files.add(ref)
    
    # 3. Lister tous les fichiers du projet
    print("\n" + "=" * 80)
    print("✅ FICHIERS NÉCESSAIRES")
    print("=" * 80)
    
    for f in sorted(necessary_files):
        if os.path.exists(f):
            size = os.path.getsize(f) / 1024
            print(f"  ✓ {f:50} ({size:.1f} KB)")
        else:
            print(f"  ⚠️ {f:50} (MANQUANT)")
    
    # 4. Trouver les fichiers inutilisés
    print("\n" + "=" * 80)
    print("🗑️ FICHIERS INUTILISÉS (peuvent être supprimés)")
    print("=" * 80)
    
    all_files = set()
    for f in os.listdir('.'):
        if f.endswith(('.py', '.js', '.html', '.json', '.bat', '.ps1', '.txt', '.md')):
            all_files.add(f)
    
    unused_files = all_files - necessary_files
    
    total_unused_size = 0
    for f in sorted(unused_files):
        if os.path.exists(f):
            size = os.path.getsize(f) / 1024
            total_unused_size += size
            print(f"  ❌ {f:50} ({size:.1f} KB)")
    
    print(f"\n📊 Total fichiers nécessaires: {len(necessary_files)}")
    print(f"📊 Total fichiers inutilisés: {len(unused_files)}")
    print(f"📊 Espace récupérable: {total_unused_size:.1f} KB")
    
    # 5. Créer un script de nettoyage
    print("\n" + "=" * 80)
    print("💾 CRÉATION DU SCRIPT DE NETTOYAGE")
    print("=" * 80)
    
    with open('cleanup_all_duplicates.bat', 'w', encoding='utf-8') as f:
        f.write('@echo off\n')
        f.write('echo ========================================\n')
        f.write('echo   NETTOYAGE COMPLET DES DUPLICATAS\n')
        f.write('echo ========================================\n')
        f.write('echo.\n')
        f.write(f'echo Fichiers a supprimer: {len(unused_files)}\n')
        f.write(f'echo Espace a recuperer: {total_unused_size:.1f} KB\n')
        f.write('echo.\n')
        f.write('pause\n\n')
        
        f.write('REM Creer le dossier archives\n')
        f.write('if not exist "archives" mkdir archives\n\n')
        
        for filename in sorted(unused_files):
            if filename.endswith(('.py', '.js', '.html', '.bat', '.ps1')):
                # Archiver les fichiers de code
                f.write(f'if exist "{filename}" move /Y "{filename}" "archives\\" >nul 2>&1\n')
            elif filename.endswith(('.json', '.txt', '.md')):
                # Supprimer les fichiers de données/config obsolètes
                if 'data_structure' in filename or 'files_data' in filename or 'html_config' in filename:
                    f.write(f'if exist "{filename}" del /Q "{filename}" >nul 2>&1\n')
                else:
                    f.write(f'if exist "{filename}" move /Y "{filename}" "archives\\" >nul 2>&1\n')
        
        f.write('\necho.\n')
        f.write('echo [OK] Nettoyage termine!\n')
        f.write('pause\n')
    
    print("  ✓ Script créé: cleanup_all_duplicates.bat")
    print("\n💡 Exécutez cleanup_all_duplicates.bat pour nettoyer")

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
