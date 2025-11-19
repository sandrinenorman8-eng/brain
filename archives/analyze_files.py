#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyse des fichiers utilisés vs inutilisés dans le projet Deuxième Cerveau
"""
import os
import re
from pathlib import Path

# Fichiers actifs (utilisés par START.bat et l'application)
ACTIVE_FILES = {
    # Core application
    'app.py': 'Main Flask application (ACTIVE)',
    'category_path_resolver.py': 'Path resolution with hierarchy (ACTIVE)',
    'index.html': 'Main UI (ACTIVE)',
    'all_notes_standalone.html': 'Standalone notes viewer (ACTIVE)',
    'search-server-fixed.js': 'Node.js search service (ACTIVE - used by START.bat)',
    'categories.json': 'Category definitions (ACTIVE)',
    'category_mapping.json': 'Hierarchical path mappings (ACTIVE)',
    
    # Startup/shutdown
    'START.bat': 'Main startup script (ACTIVE)',
    'STOP.bat': 'Shutdown script (ACTIVE)',
    
    # Configuration
    'requirements.txt': 'Python dependencies (ACTIVE)',
    'package.json': 'Node.js metadata (ACTIVE)',
    'pyrightconfig.json': 'Python type checking config (ACTIVE)',
    
    # Utilities
    'cleanup_empty_folders.py': 'Utility to clean empty folders (ACTIVE)',
    'verify_endpoints.py': 'Endpoint verification (ACTIVE)',
    'update_notes_data.bat': 'Update notes cache (ACTIVE)',
    
    # Backup
    'BACKUP_COMPLET.bat': 'Complete backup script (ACTIVE - root level)',
}

# Fichiers de backup/debug (potentiellement inutiles)
BACKUP_DEBUG_FILES = {
    'app_backup.py': 'BACKUP - Old version of app.py',
    'app_backup_before_subfolder_support.py': 'BACKUP - Before subfolder support',
    'app_before_mapping.py': 'BACKUP - Before category mapping',
    'app_test.py': 'DEBUG/TEST - App testing',
    'index.html.backup': 'BACKUP - Old index.html',
    'index_final_stable_20250919_084153.html': 'BACKUP - Stable version from Sept 2025',
    'START.bat.backup': 'BACKUP - Old START.bat',
    'START_original.bat': 'BACKUP - Original START.bat',
    'search-server.js': 'DUPLICATE - search-server-fixed.js is used instead',
}

# Fichiers de debug JavaScript
DEBUG_JS_FILES = {
    'check_alphabet_container.js': 'DEBUG - Check alphabet container',
    'check_api_calls.js': 'DEBUG - Check API calls',
    'check_buttons_visible.js': 'DEBUG - Check button visibility',
    'check_server_files.js': 'DEBUG - Check server files',
    'debug_all_notes.js': 'DEBUG - Debug all notes',
    'debug_alphabet_buttons.js': 'DEBUG - Debug alphabet buttons',
    'debug_buttons_detailed.js': 'DEBUG - Debug buttons detailed',
    'debug_integration.js': 'DEBUG - Debug integration',
    'debug_server_start.js': 'DEBUG - Debug server start',
    'debug_small_buttons.js': 'DEBUG - Debug small buttons',
    'diagnostic_complet.js': 'DEBUG - Complete diagnostic',
    'diagnostic_ultime.js': 'DEBUG - Ultimate diagnostic',
    'fix_modal_buttons.js': 'DEBUG - Fix modal buttons',
    'modal_buttons_fix_summary.js': 'DEBUG - Modal buttons fix summary',
}

# Fichiers Python utilitaires (potentiellement inutilisés)
UTILITY_PYTHON_FILES = {
    'debug_index.py': 'DEBUG - Debug index',
    'ensure_html_consistency.py': 'UTILITY - Ensure HTML consistency',
    'extract_assets.py': 'UTILITY - Extract assets',
    'generate_notes_data.py': 'UTILITY - Generate notes data',
    'html_template_generator.py': 'UTILITY - HTML template generator',
    'monitor.py': 'UTILITY - Monitor (check if used)',
    'organize_data_folders.py': 'UTILITY - Organize data folders',
    'routes_fusion.py': 'UTILITY - Fusion routes (check if imported)',
    'routes_structured.py': 'UTILITY - Structured routes (check if imported)',
    'validate_html_consistency.py': 'UTILITY - Validate HTML consistency',
    'verify_upload_implementation.py': 'UTILITY - Verify upload implementation',
}

# Fichiers de données/config (potentiellement obsolètes)
DATA_CONFIG_FILES = {
    'data_structure.json': 'CONFIG - Data structure (check if used)',
    'files_data.json': 'DATA - Files data cache (check if used)',
    'folder_hierarchy.json': 'CONFIG - Folder hierarchy (check if used)',
    'html_config.json': 'CONFIG - HTML config (check if used)',
}

# Autres fichiers
OTHER_FILES = {
    'notes_launcher.html': 'HTML - Notes launcher (check if used)',
    'lancer_deuxieme_cerveau.bat': 'BAT - Alternative launcher (duplicate of START.bat?)',
    'demarrer_recherche.bat': 'BAT - Start search (check if used)',
    'open_all_notes_test.bat': 'BAT - Test script',
    'start_search_server.bat': 'BAT - Start search server (duplicate?)',
    'start_deuxieme_cerveau.ps1': 'PS1 - PowerShell launcher (duplicate?)',
    'TEST_MIGRATION.bat': 'BAT - Migration test',
    'monitor.log': 'LOG - Monitor log file',
    'server.err.log': 'LOG - Server error log',
    'server.log': 'LOG - Server log',
    'server.out.log': 'LOG - Server output log',
    'server.pid': 'PID - Server process ID',
    'node': 'UNKNOWN - Check what this is',
}

def check_file_imports(filepath):
    """Check if a file is imported/used by other files"""
    filename = os.path.basename(filepath)
    base_name = filename.replace('.py', '').replace('.js', '')
    
    # Search for imports in Python files
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.venv', 'node_modules', 'backups', 'archives']]
        
        for file in files:
            if file.endswith(('.py', '.js', '.bat', '.html')):
                try:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        # Check for various import patterns
                        patterns = [
                            f'import {base_name}',
                            f'from {base_name}',
                            f'require.*{base_name}',
                            f'{filename}',
                        ]
                        
                        for pattern in patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                return True, file
                except:
                    pass
    
    return False, None

def analyze_files():
    """Analyze all files and categorize them"""
    print("=" * 80)
    print("ANALYSE DES FICHIERS - DEUXIÈME CERVEAU")
    print("=" * 80)
    print()
    
    print("✅ FICHIERS ACTIFS (utilisés par l'application)")
    print("-" * 80)
    for filename, description in sorted(ACTIVE_FILES.items()):
        status = "✓" if os.path.exists(filename) else "✗ MANQUANT"
        print(f"  {status} {filename:40} - {description}")
    print()
    
    print("🔄 FICHIERS DE BACKUP/ANCIENNES VERSIONS (potentiellement inutiles)")
    print("-" * 80)
    for filename, description in sorted(BACKUP_DEBUG_FILES.items()):
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024
            print(f"  📦 {filename:40} - {description} ({size:.1f} KB)")
    print()
    
    print("🐛 FICHIERS DE DEBUG JAVASCRIPT (potentiellement inutiles)")
    print("-" * 80)
    for filename, description in sorted(DEBUG_JS_FILES.items()):
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024
            print(f"  🔍 {filename:40} - {description} ({size:.1f} KB)")
    print()
    
    print("🔧 FICHIERS PYTHON UTILITAIRES (vérifier l'utilisation)")
    print("-" * 80)
    for filename, description in sorted(UTILITY_PYTHON_FILES.items()):
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024
            is_used, used_by = check_file_imports(filename)
            status = f"UTILISÉ par {used_by}" if is_used else "NON UTILISÉ"
            print(f"  🛠️  {filename:40} - {description} ({size:.1f} KB) - {status}")
    print()
    
    print("📊 FICHIERS DE DONNÉES/CONFIG (vérifier l'utilisation)")
    print("-" * 80)
    for filename, description in sorted(DATA_CONFIG_FILES.items()):
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024
            is_used, used_by = check_file_imports(filename)
            status = f"UTILISÉ par {used_by}" if is_used else "NON UTILISÉ"
            print(f"  📄 {filename:40} - {description} ({size:.1f} KB) - {status}")
    print()
    
    print("❓ AUTRES FICHIERS (vérifier l'utilisation)")
    print("-" * 80)
    for filename, description in sorted(OTHER_FILES.items()):
        if os.path.exists(filename):
            try:
                size = os.path.getsize(filename) / 1024
                print(f"  ❔ {filename:40} - {description} ({size:.1f} KB)")
            except:
                print(f"  ❔ {filename:40} - {description} (erreur lecture)")
    print()
    
    # Calculate total size of potentially unused files
    total_backup_size = sum(os.path.getsize(f) for f in BACKUP_DEBUG_FILES.keys() if os.path.exists(f))
    total_debug_size = sum(os.path.getsize(f) for f in DEBUG_JS_FILES.keys() if os.path.exists(f))
    
    print("=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)
    print(f"Fichiers de backup/anciennes versions: {total_backup_size / 1024:.1f} KB")
    print(f"Fichiers de debug JavaScript: {total_debug_size / 1024:.1f} KB")
    print(f"Total potentiellement supprimable: {(total_backup_size + total_debug_size) / 1024:.1f} KB")
    print()
    
    # Recommendations
    print("💡 RECOMMANDATIONS")
    print("-" * 80)
    print("1. Les fichiers de BACKUP peuvent être archivés ou supprimés")
    print("2. Les fichiers de DEBUG JavaScript peuvent être supprimés (ou archivés)")
    print("3. Vérifier les fichiers UTILITY Python pour voir s'ils sont importés")
    print("4. Les fichiers LOG (.log, .pid) peuvent être nettoyés régulièrement")
    print("5. search-server.js est un DUPLICATE de search-server-fixed.js")
    print()

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    analyze_files()
