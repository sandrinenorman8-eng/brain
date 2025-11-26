from flask import Blueprint, send_from_directory, jsonify, request, make_response, render_template
import os
import re
import glob
from datetime import datetime
from services.notes_service import get_all_files, extract_file_creation_hour
from utils.file_utils import safe_read
from category_path_resolver import get_category_path
from services.category_service import load_categories

web_bp = Blueprint('web', __name__)

# Obtenir le répertoire de base de l'application
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@web_bp.route('/')
@web_bp.route('/index.html')
def index():
    try:
        from flask import make_response
        response = make_response(send_from_directory(BASE_DIR, 'index.html'))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        return f"Error serving index.html: {e}", 500

@web_bp.route('/all_notes')
def all_notes():
    try:
        return send_from_directory(BASE_DIR, 'all_notes_standalone.html')
    except Exception as e:
        return f"Error loading page: {e}", 500

@web_bp.route('/all_notes_data')
def all_notes_data():
    try:
        all_files_data = get_all_files()
        
        categories_data = {}
        for item in all_files_data:
            category_name = item['category']
            if category_name not in categories_data:
                categories_data[category_name] = {
                    'name': category_name,
                    'emoji': item['emoji'],
                    'color': item['color'],
                    'files': [],
                    'latest_file_date': item['date'],
                    'latest_file_hour': item.get('hour', '00:00:00')
                }
            
            file_hour = extract_file_creation_hour(category_name, item['filename'])
            
            categories_data[category_name]['files'].append({
                'filename': item['filename'],
                'date': item['date'],
                'hour': file_hour
            })
            
            current_latest_date = categories_data[category_name]['latest_file_date']
            if item['date'] > current_latest_date:
                categories_data[category_name]['latest_file_date'] = item['date']
                categories_data[category_name]['latest_file_hour'] = file_hour or '00:00:00'
            elif item['date'] == current_latest_date:
                current_hour = categories_data[category_name].get('latest_file_hour', '00:00:00')
                if (file_hour or '00:00:00') > current_hour:
                    categories_data[category_name]['latest_file_hour'] = file_hour or '00:00:00'
            
            if 'latest_file_hour' not in categories_data[category_name]:
                categories_data[category_name]['latest_file_hour'] = file_hour or '00:00:00'
        
        sorted_categories = sorted(categories_data.items(),
                                 key=lambda x: (x[1]['latest_file_date'], x[1].get('latest_file_hour', '00:00:00')),
                                 reverse=True)
        
        categories_html = ""
        for i, (cat_name, cat_data) in enumerate(sorted_categories):
            files_html = ""
            for file in cat_data['files']:
                date_formatted = file['date'].split('-')
                if len(date_formatted) == 3:
                    date_formatted = f"{date_formatted[2]}/{date_formatted[1]}/{date_formatted[0]}"
                else:
                    date_formatted = file['date']
                
                if file.get('hour') and file['hour'] != '00:00:00':
                    display_date = f"{date_formatted} à {file['hour']}"
                else:
                    display_date = date_formatted
                
                files_html += f"""
                <div class="file-item">
                    <div class="file-info">
                        <span class="file-emoji">📄</span>
                        <span class="file-name">{file['filename']}</span>
                        <span class="file-date">{display_date}</span>
                    </div>
                    <a href="/api/read/{cat_name}/{file['filename']}" target="_blank" class="read-btn">Lire</a>
                </div>
                """
            
            latest_date_formatted = cat_data['latest_file_date'].split('-')
            if len(latest_date_formatted) == 3:
                latest_date_display = f"{latest_date_formatted[2]}/{latest_date_formatted[1]}/{latest_date_formatted[0]}"
                if cat_data.get('latest_file_hour') and cat_data['latest_file_hour'] != '00:00:00':
                    latest_date_display += f" à {cat_data['latest_file_hour']}"
            else:
                latest_date_display = cat_data['latest_file_date']
            
            categories_html += f"""
            <div class="accordion-item">
                <button class="accordion-header" onclick="toggleAccordion('content-{cat_name.replace(' ', '-')}')">
                    <div class="folder-info">
                        <span class="folder-emoji">{cat_data['emoji']}</span>
                        <span class="folder-name">{cat_name}</span>
                        <span class="file-count">{len(cat_data['files'])} fichier{'s' if len(cat_data['files']) > 1 else ''}</span>
                        <span class="latest-date">Dernier: {latest_date_display}</span>
                    </div>
                    <span class="accordion-icon" id="icon-content-{cat_name.replace(' ', '-')}">▼</span>
                </button>
                <div class="accordion-content" id="content-{cat_name.replace(' ', '-')}">
                    <div class="files-container">
                        {files_html}
                    </div>
                </div>
            </div>
            """
        
        return jsonify({
            'html': categories_html,
            'categories_count': len(sorted_categories),
            'total_files': len(all_files_data)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@web_bp.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'static'), filename)

@web_bp.route('/static/node_modules/<path:filename>')
def serve_node_modules(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'node_modules'), filename)

# Routes de compatibilité pour le frontend - SUPPRIMÉE car dupliquée dans category_routes.py

@web_bp.route('/categories_structured')
def categories_structured():
    """Returns categories with hierarchical structure (parents/children)"""
    try:
        from services.category_service import load_categories
        import json
        
        categories = load_categories()
        
        # Load mapping
        mapping = {}
        mapping_file = os.path.join(BASE_DIR, 'category_mapping.json')
        if os.path.exists(mapping_file):
            with open(mapping_file, 'r', encoding='utf-8') as f:
                mapping = json.load(f)
        
        # Parent folder definitions
        parent_folders = {
            "buziness": {"emoji": "💼", "color": "#f59e0b"},
            "cinema": {"emoji": "🎬", "color": "#ef4444"},
            "livres": {"emoji": "📚", "color": "#8b5cf6"},
            "logiciels": {"emoji": "💻", "color": "#3b82f6"},
            "series": {"emoji": "📺", "color": "#ec4899"},
            "priorité": {"emoji": "🚀", "color": "#10b981"}
        }
        
        structured = {"parents": [], "standalone": []}
        parent_children = {}
        
        for cat in categories:
            cat_name = cat['name']
            cat_path = mapping.get(cat_name, cat_name)
            
            if '/' in cat_path:
                parent_name = cat_path.split('/')[0]
                if parent_name not in parent_children:
                    parent_info = parent_folders.get(parent_name, {"emoji": "📁", "color": "#6b7280"})
                    parent_children[parent_name] = {
                        "name": parent_name,
                        "emoji": parent_info["emoji"],
                        "color": parent_info["color"],
                        "children": [],
                        "isParent": True
                    }
                parent_children[parent_name]["children"].append({
                    "name": cat_name,
                    "emoji": cat['emoji'],
                    "color": cat['color'],
                    "path": cat_path,
                    "isChild": True
                })
            else:
                structured["standalone"].append({
                    "name": cat_name,
                    "emoji": cat['emoji'],
                    "color": cat['color'],
                    "path": cat_path,
                    "isStandalone": True
                })
        
        structured["parents"] = list(parent_children.values())
        for parent in structured["parents"]:
            parent["children"].sort(key=lambda x: x['name'])
        
        return jsonify(structured)
    except Exception as e:
        print(f"Error in categories_structured: {e}")
        return jsonify({"parents": [], "standalone": []}), 500

@web_bp.route('/folder_hierarchy')
def folder_hierarchy():
    """Return folder hierarchy for UI rendering"""
    try:
        # Load category mapping to get hierarchy
        import json
        mapping_file = os.path.join(BASE_DIR, 'category_mapping.json')
        
        if os.path.exists(mapping_file):
            with open(mapping_file, 'r', encoding='utf-8') as f:
                mapping = json.load(f)
            
            # Build hierarchy from mapping
            hierarchy = {}
            for category, path in mapping.items():
                parts = path.split('/')
                if len(parts) > 1:
                    parent = parts[0]
                    if parent not in hierarchy:
                        hierarchy[parent] = []
                    hierarchy[parent].append(category)
            
            return jsonify(hierarchy)
        else:
            return jsonify({})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@web_bp.route('/fusionner')
def fusionner():
    """Fusionne tous les fichiers d'un dossier spécifique et retourne le HTML (EXACTEMENT comme le backup)"""
    try:
        dossier = request.args.get('dossier', '').strip()
        
        if not dossier:
            return "Paramètre 'dossier' manquant", 400
        
        # Vérifier que la catégorie existe
        categories = load_categories()
        if not any(c['name'] == dossier for c in categories):
            return f"Catégorie '{dossier}' introuvable", 404
        
        # Get the actual folder path
        full_path = get_category_path(dossier)
        
        if not os.path.exists(full_path):
            return f"Dossier '{dossier}' n'existe pas", 404
        
        # Récupérer tous les fichiers du dossier
        files = [f for f in os.listdir(full_path)
                if f.startswith(f'{dossier}_') and f.endswith('.txt')]
        
        if not files:
            return f"Aucun fichier trouvé dans '{dossier}'", 404
        
        # Trier les fichiers par date (du plus récent au plus ancien)
        files.sort(reverse=True)
        
        # Fusionner tous les fichiers
        merged_content = []
        for filename in files:
            filepath = os.path.join(full_path, filename)
            try:
                content = safe_read(filepath)
                
                # Ajouter un en-tête pour chaque fichier
                merged_content.append(f"\n{'='*60}")
                merged_content.append(f"📄 FICHIER: {filename}")
                merged_content.append(f"{'='*60}\n")
                merged_content.append(content)
                merged_content.append("\n")
            except Exception as e:
                print(f"Erreur lors de la lecture de {filepath}: {e}")
                merged_content.append(f"\n{'='*60}")
                merged_content.append(f"📄 FICHIER: {filename} (ERREUR)")
                merged_content.append(f"{'='*60}\n")
                merged_content.append(f"❌ Erreur de lecture: {str(e)}\n\n")
        
        final_content = '\n'.join(merged_content)
        
        # Fonction pour surligner les dates
        def highlight_dates(content):
            patterns = [
                r'\b\d{4}-\d{2}-\d{2}\b',
                r'\b\d{1,2}/\d{1,2}/\d{4}\b',
                r'\b\d{1,2}-\d{1,2}-\d{4}\b',
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
                r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
                r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b',
                r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b'
            ]
            date_pattern = '|'.join(patterns)
            
            def replace_date(match):
                date_text = match.group(0)
                return f'<span style="color: #ff6b6b; font-weight: bold;">{date_text}</span>'
            
            return re.sub(date_pattern, replace_date, content, flags=re.IGNORECASE)
        
        # Fonction pour surligner les nombres
        def highlight_numbers(content):
            number_pattern = r'\d{1,2}:\d{2}(?::\d{2})?|\b\d+(?:\.\d+)?\b'
            
            def replace_number(match):
                number_text = match.group(0)
                return f'<span style="color: #ef4444; font-weight: bold;">{number_text}</span>'
            
            return re.sub(number_pattern, replace_number, content)
        
        # Surligner les dates et les nombres
        highlighted_content = highlight_dates(final_content)
        highlighted_content = highlight_numbers(highlighted_content)
        
        # Générer le HTML avec le style dark mode (EXACTEMENT comme le backup)
        html_template = f"""
<!DOCTYPE html>
<html class="dark" lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fusion - {dossier}</title>
    <link href="https://fonts.googleapis.com" rel="preconnect"/>
    <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap" rel="stylesheet"/>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <script>
      tailwind.config = {{
        darkMode: 'class',
        theme: {{
          extend: {{
            colors: {{
              primary: '#137fec',
              'background-light': '#f6f7f8',
              'background-dark': '#101922',
            }},
            fontFamily: {{ display: ['Inter'] }},
            borderRadius: {{ DEFAULT: '0.25rem', lg: '0.5rem', xl: '0.75rem', full: '9999px' }},
          }},
        }},
      }}
    </script>
</head>
<body class="font-display bg-background-light dark:bg-background-dark text-stone-800 dark:text-stone-200">
  <div class="flex flex-col min-h-screen">
    <header class="sticky top-0 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-sm z-10">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16 border-b border-stone-200 dark:border-stone-800">
          <div class="flex items-center gap-4">
            <div class="text-primary size-7">
              <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M42.4379 44C42.4379 44 36.0744 33.9038 41.1692 24C46.8624 12.9336 42.2078 4 42.2078 4L7.01134 4C7.01134 4 11.6577 12.932 5.96912 23.9969C0.876273 33.9029 7.27094 44 7.27094 44L42.4379 44Z" fill="currentColor"></path></svg>
            </div>
            <h1 class="text-xl font-bold text-stone-900 dark:text-white">Fusion - {dossier}</h1>
          </div>
        </div>
      </div>
    </header>

    <main class="flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="max-w-4xl mx-auto space-y-6">
        <div class="bg-white dark:bg-stone-800 rounded-lg shadow-md border border-stone-200 dark:border-stone-700 p-6">
          <div class="text-sm text-stone-600 dark:text-stone-400 mb-4">📊 Dossier: <strong>{dossier}</strong> · Fichiers fusionnés: <strong>{len(files)}</strong> · Généré: <strong>{datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</strong></div>
          <div class="prose prose-stone dark:prose-invert max-w-none" style="white-space: pre-wrap;">{highlighted_content}</div>
        </div>
        <div class="text-center"><a href="javascript:window.close()" class="inline-flex items-center bg-primary text-white rounded-md px-4 py-2 text-sm hover:bg-primary/90 transition-colors">← Fermer cette fenêtre</a></div>
      </div>
    </main>
  </div>
</body>
</html>
"""
        
        resp = make_response(html_template)
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp
        
    except Exception as e:
        print(f"Erreur lors de la fusion du dossier {dossier}: {str(e)}")
        return f"Erreur: {str(e)}", 500

@web_bp.route('/view_fusion_global')
def view_fusion_global():
    """Liste tous les fichiers du dossier fusion_global avec liens cliquables"""
    try:
        fusion_global_dir = os.path.join(BASE_DIR, 'fusion_global')
        
        if not os.path.exists(fusion_global_dir):
            return "Le dossier fusion_global n'existe pas", 404
        
        # Get all files in fusion_global directory
        all_files = []
        for filename in os.listdir(fusion_global_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(fusion_global_dir, filename)
                file_stat = os.stat(filepath)
                all_files.append({
                    'name': filename,
                    'size': file_stat.st_size,
                    'mtime': file_stat.st_mtime,
                    'date_str': datetime.fromtimestamp(file_stat.st_mtime).strftime('%d/%m/%Y à %H:%M:%S')
                })
        
        # Sort by modification time (most recent first)
        all_files.sort(key=lambda x: x['mtime'], reverse=True)
        
        # Generate file list HTML
        files_html = ""
        for file in all_files:
            size_kb = file['size'] / 1024
            files_html += f"""
            <div class="file-item p-4 mb-3 rounded-lg border border-pink-500/30 hover:border-pink-500/60 hover:bg-pink-500/10 transition-all">
                <div class="flex items-center justify-between">
                    <div class="flex-1">
                        <div class="text-white font-medium">{file['name']}</div>
                        <div class="text-sm text-gray-400">
                            <span class="text-pink-400">{file['date_str']}</span> · {size_kb:.1f} KB
                        </div>
                    </div>
                    <a href="/read_fusion_file/fusion_global/{file['name']}" target="_blank"
                       class="px-4 py-2 bg-pink-500 hover:bg-pink-600 text-white rounded-lg transition-colors">
                        📖 Lire
                    </a>
                </div>
            </div>
            """
        
        # Generate HTML
        html_template = f"""
<!DOCTYPE html>
<html class="dark" lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📖 Fusion Globale - Deuxième Cerveau</title>
    <link href="https://fonts.googleapis.com" rel="preconnect"/>
    <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&family=Orbitron:wght@400;700&display=swap" rel="stylesheet"/>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <style>
        body {{
            background: linear-gradient(135deg, #1a0a1a 0%, #2e1a2e 100%);
            font-family: 'Manrope', sans-serif;
        }}
        h1, h2 {{
            font-family: 'Orbitron', sans-serif;
        }}
        .content-box {{
            background: rgba(42, 13, 42, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 0, 229, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        .text-glow {{
            text-shadow: 0 0 10px rgba(255, 0, 229, 0.8);
        }}
    </style>
</head>
<body class="text-white min-h-screen">
    <div class="container mx-auto px-4 py-8 max-w-6xl">
        <header class="mb-8 text-center">
            <h1 class="text-4xl font-bold text-glow mb-2">📖 Fusion Globale</h1>
            <p class="text-gray-400">Dossier: <span class="text-pink-400">fusion_global/</span></p>
            <p class="text-gray-400">Total: <span class="text-pink-400">{len(all_files)} fichiers</span></p>
        </header>
        
        <main class="content-box rounded-xl p-8 mb-8">
            {files_html if files_html else '<p class="text-center text-gray-400">Aucun fichier trouvé</p>'}
        </main>
        
        <footer class="text-center">
            <button onclick="window.close()" 
                    class="px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 
                           text-white font-bold rounded-lg shadow-lg transition-all duration-300 transform hover:scale-105">
                ← Fermer cette fenêtre
            </button>
        </footer>
    </div>
</body>
</html>
"""
        
        resp = make_response(html_template)
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp
        
    except Exception as e:
        print(f"Erreur lors de l'affichage de la fusion globale: {str(e)}")
        return f"Erreur: {str(e)}", 500

@web_bp.route('/read_fusion_file/<folder>/<filename>')
def read_fusion_file(folder, filename):
    """Lit et affiche un fichier de fusion spécifique"""
    try:
        # Security check
        if folder not in ['fusion_global', 'fusion_categories']:
            return "Dossier non autorisé", 403
        
        file_path = os.path.join(BASE_DIR, folder, filename)
        
        if not os.path.exists(file_path):
            return "Fichier introuvable", 404
        
        # Read content
        content = safe_read(file_path)
        
        # Escape HTML but preserve line breaks
        import html
        content_escaped = html.escape(content)
        
        # Highlight dates in pink
        content_escaped = re.sub(
            r'\b(\d{1,2}/\d{1,2}/\d{4})\b',
            r'<span style="color: #ff00e5; font-weight: bold;">\1</span>',
            content_escaped
        )
        
        # Highlight times in cyan
        content_escaped = re.sub(
            r'\b(\d{1,2}:\d{2}:\d{2})\b',
            r'<span style="color: #00f6ff; font-weight: bold;">\1</span>',
            content_escaped
        )
        
        # Generate HTML
        html_template = f"""
<!DOCTYPE html>
<html class="dark" lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{filename} - Deuxième Cerveau</title>
    <link href="https://fonts.googleapis.com" rel="preconnect"/>
    <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&family=Orbitron:wght@400;700&display=swap" rel="stylesheet"/>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <style>
        body {{
            background: linear-gradient(135deg, #1a0a1a 0%, #2e1a2e 100%);
            font-family: 'Manrope', sans-serif;
        }}
        h1, h2 {{
            font-family: 'Orbitron', sans-serif;
        }}
        .content-box {{
            background: rgba(42, 13, 42, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 0, 229, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        .text-glow {{
            text-shadow: 0 0 10px rgba(255, 0, 229, 0.8);
        }}
    </style>
</head>
<body class="text-white min-h-screen">
    <div class="container mx-auto px-4 py-8 max-w-6xl">
        <header class="mb-8 text-center">
            <h1 class="text-3xl font-bold text-glow mb-2">📄 {filename}</h1>
            <p class="text-gray-400">Dossier: <span class="text-pink-400">{folder}/</span></p>
        </header>
        
        <main class="content-box rounded-xl p-8 mb-8">
            <div class="prose prose-invert max-w-none" style="white-space: pre-wrap; line-height: 1.8; font-size: 16px;">
{content_escaped}
            </div>
        </main>
        
        <footer class="text-center">
            <button onclick="window.close()" 
                    class="px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 
                           text-white font-bold rounded-lg shadow-lg transition-all duration-300 transform hover:scale-105">
                ← Fermer cette fenêtre
            </button>
        </footer>
    </div>
</body>
</html>
"""
        
        resp = make_response(html_template)
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp
        
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {str(e)}")
        return f"Erreur: {str(e)}", 500

@web_bp.route('/view_fusion_categories')
def view_fusion_categories():
    """Liste tous les fichiers du dossier fusion_categories ORGANISÉS PAR CATÉGORIE"""
    try:
        fusion_categories_dir = os.path.join(BASE_DIR, 'fusion_categories')
        
        if not os.path.exists(fusion_categories_dir):
            return "Le dossier fusion_categories n'existe pas", 404
        
        # Get all files and organize by category
        categories_dict = {}
        
        for filename in os.listdir(fusion_categories_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(fusion_categories_dir, filename)
                file_stat = os.stat(filepath)
                
                # Extract category from filename
                # Format: fusion_categories_CATEGORY_DATE.txt or fusion_CATEGORY_DATE.txt
                # Date format: YYYY-MM-DD_HH-MM-SS
                category = "Autres"
                
                # Remove extension
                name_without_ext = filename.replace('.txt', '')
                
                # Remove date pattern (YYYY-MM-DD_HH-MM-SS) from the end
                import re
                name_without_date = re.sub(r'_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$', '', name_without_ext)
                
                # Extract category
                if name_without_date.startswith('fusion_categories_'):
                    category = name_without_date.replace('fusion_categories_', '')
                elif name_without_date.startswith('fusion_'):
                    category = name_without_date.replace('fusion_', '')
                
                # Capitalize category name
                category = category.upper()
                
                if category not in categories_dict:
                    categories_dict[category] = []
                
                categories_dict[category].append({
                    'name': filename,
                    'size': file_stat.st_size,
                    'mtime': file_stat.st_mtime,
                    'date_str': datetime.fromtimestamp(file_stat.st_mtime).strftime('%d/%m/%Y à %H:%M:%S')
                })
        
        # Sort categories alphabetically and files by date
        sorted_categories = sorted(categories_dict.items())
        for category, files in sorted_categories:
            files.sort(key=lambda x: x['mtime'], reverse=True)
        
        # Generate HTML for each category
        categories_html = ""
        total_files = 0
        
        for category, files in sorted_categories:
            total_files += len(files)
            files_html = ""
            
            for file in files:
                size_kb = file['size'] / 1024
                files_html += f"""
                <div class="file-item p-3 mb-2 rounded-lg border border-pink-500/20 hover:border-pink-500/50 hover:bg-pink-500/5 transition-all">
                    <div class="flex items-center justify-between">
                        <div class="flex-1">
                            <div class="text-white text-sm">{file['name']}</div>
                            <div class="text-xs text-gray-400">
                                <span class="text-pink-400">{file['date_str']}</span> · {size_kb:.1f} KB
                            </div>
                        </div>
                        <a href="/read_fusion_file/fusion_categories/{file['name']}" target="_blank"
                           class="px-3 py-1 bg-pink-500 hover:bg-pink-600 text-white text-sm rounded-lg transition-colors">
                            📖 Lire
                        </a>
                    </div>
                </div>
                """
            
            categories_html += f"""
            <div class="category-section mb-6">
                <h2 class="text-2xl font-bold text-pink-400 mb-4 flex items-center">
                    <span class="mr-2">📁</span> {category.upper()}
                    <span class="ml-3 text-sm text-gray-400 font-normal">({len(files)} fichiers)</span>
                </h2>
                <div class="ml-4">
                    {files_html}
                </div>
            </div>
            """
        
        # Generate HTML
        html_template = f"""
<!DOCTYPE html>
<html class="dark" lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📚 Fusion Catégories - Deuxième Cerveau</title>
    <link href="https://fonts.googleapis.com" rel="preconnect"/>
    <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&family=Orbitron:wght@400;700&display=swap" rel="stylesheet"/>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <style>
        body {{
            background: linear-gradient(135deg, #1a0a1a 0%, #2e1a2e 100%);
            font-family: 'Manrope', sans-serif;
        }}
        h1, h2 {{
            font-family: 'Orbitron', sans-serif;
        }}
        .content-box {{
            background: rgba(42, 13, 42, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 0, 229, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        .text-glow {{
            text-shadow: 0 0 10px rgba(255, 0, 229, 0.8);
        }}
    </style>
</head>
<body class="text-white min-h-screen">
    <div class="container mx-auto px-4 py-8 max-w-6xl">
        <header class="mb-8 text-center">
            <h1 class="text-4xl font-bold text-glow mb-2">📚 Fusion par Catégories</h1>
            <p class="text-gray-400">Dossier: <span class="text-pink-400">fusion_categories/</span></p>
            <p class="text-gray-400">Total: <span class="text-pink-400">{total_files} fichiers</span> · <span class="text-pink-400">{len(sorted_categories)} catégories</span></p>
        </header>
        
        <main class="content-box rounded-xl p-8 mb-8">
            {categories_html if categories_html else '<p class="text-center text-gray-400">Aucun fichier trouvé</p>'}
        </main>
        
        <footer class="text-center">
            <button onclick="window.close()" 
                    class="px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 
                           text-white font-bold rounded-lg shadow-lg transition-all duration-300 transform hover:scale-105">
                ← Fermer cette fenêtre
            </button>
        </footer>
    </div>
</body>
</html>
"""
        
        resp = make_response(html_template)
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp
        
    except Exception as e:
        print(f"Erreur lors de l'affichage de la fusion par catégories: {str(e)}")
        return f"Erreur: {str(e)}", 500


@web_bp.route('/fusion_intelligente')
def fusion_intelligente():
    """Page de fusion intelligente avec IA"""
    try:
        return send_from_directory(BASE_DIR, 'fusion_intelligente.html')
    except Exception as e:
        return f"Error loading page: {e}", 500

@web_bp.route('/knowledge_graph')
def knowledge_graph():
    """Page du knowledge graph"""
    try:
        return render_template('knowledge_graph.html')
    except Exception as e:
        return f"Error loading page: {e}", 500
