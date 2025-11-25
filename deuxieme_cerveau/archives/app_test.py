from flask import Flask, request, jsonify
import os
from datetime import datetime
import json
import random
import zipfile
import shutil
from functools import lru_cache

app = Flask(__name__)

CATEGORIES_FILE = "categories.json"

# Liste d'emojis pour la sélection aléatoire lors de la création de nouvelles catégories
EMOJIS = ["📁", "📄", "📝", "💡", "🚀", "🌟", "📚", "📌", "⚙️", "✅", "🎯", "🔧", "📊", "🎨", "🔍", "💼", "📈", "🎪", "🔮", "⭐"]

@lru_cache(maxsize=1)
def load_categories():
    if not os.path.exists(CATEGORIES_FILE):
        default_categories = [
            {"name": "scénario", "emoji": "🎬", "color": "#FF6B6B"},
            {"name": "actualité", "emoji": "🗞", "color": "#4ECDC4"},
            {"name": "idées", "emoji": "💡", "color": "#45B7D1"},
            {"name": "projets", "emoji": "🏗", "color": "#FFA94D"},
            {"name": "recherche", "emoji": "🔍", "color": "#6A4C93"},
            {"name": "todo", "emoji": "✅", "color": "#10B981"}
        ]
        save_categories(default_categories)
        return default_categories
    try:
        with open(CATEGORIES_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_categories(categories):
    with open(CATEGORIES_FILE, "w", encoding='utf-8') as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
    # Invalider le cache après sauvegarde
    load_categories.cache_clear()

@app.route('/save/<category>', methods=['POST'])
def save_note(category):
    data = request.json.get('text', '')
    os.makedirs(category, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    # Utiliser le nom de la catégorie au lieu de "notes" pour une meilleure organisation
    filename = f"{category}/{category}_{date_str}.txt"
    with open(filename, "a", encoding='utf-8') as f:
        time_str = datetime.now().strftime("%H:%M:%S")
        f.write(f"{time_str}: {data}\n")
    # Invalider le cache des fichiers
    _get_all_files_cached.cache_clear()
    return jsonify({"status": "saved"})

@app.route('/list/<category>')
def list_files(category):
    if not os.path.exists(category):
        return jsonify([])
    # Chercher les fichiers qui commencent par le nom de la catégorie
    files = [f for f in os.listdir(category)
            if f.startswith(f'{category}_') and f.endswith('.txt')]
    files.sort(reverse=True)
    return jsonify(files)

@lru_cache(maxsize=1)
def _get_all_files_cached():
    """Version cachée de all_files pour optimiser les performances"""
    categories = load_categories()
    all_files_data = []

    for cat in categories:
        if os.path.exists(cat['name']):
            # Chercher les fichiers qui commencent par le nom de la catégorie
            files = [f for f in os.listdir(cat['name'])
                    if f.startswith(f"{cat['name']}_") and f.endswith('.txt')]
            for file in files:
                all_files_data.append({
                    'category': cat['name'],
                    'emoji': cat['emoji'],
                    'color': cat['color'],
                    'filename': file,
                    'date': file.replace(f"{cat['name']}_", '').replace('.txt', '')
                })

    # Trier par date décroissante
    all_files_data.sort(key=lambda x: x['date'], reverse=True)
    return all_files_data

@app.route('/all_files')
def all_files():
    """Retourne tous les fichiers de toutes les catégories (optimisé avec cache)"""
    return jsonify(_get_all_files_cached())

@app.route('/read/<category>/<filename>')
def read_file(category, filename):
    if '..' in filename or '/' in filename or '\\' in filename:
        return "Nom de fichier invalide", 400
    filepath = f"{category}/{filename}"
    if not os.path.exists(filepath):
        return "Fichier non trouvé", 404

    # Essayer différents encodages pour lire le fichier
    encodings_to_try = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
    content = None

    for encoding in encodings_to_try:
        try:
            with open(filepath, "r", encoding=encoding) as f:
                content = f.read()
            break  # Si ça marche, on sort de la boucle
        except UnicodeDecodeError:
            continue  # Essayer le prochain encodage

    # Si aucun encodage n'a fonctionné, essayer en mode erreur ignorée
    if content is None:
        try:
            with open(filepath, "r", encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception:
            return "Erreur lors de la lecture du fichier", 500

    date_formatted = filename.replace(f'{category}_', '').replace('.txt', '').split('-')
    date_formatted = f"{date_formatted[2]}/{date_formatted[1]}/{date_formatted[0]}"

    # Trouver la catégorie pour l'emoji et la couleur
    categories = load_categories()
    cat_info = next((c for c in categories if c['name'] == category), {'emoji': '📁', 'color': '#666'})

    return f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{category} - {filename}</title>
        <style>
            body {{
                font-family: sans-serif;
                padding: 20px;
                max-width: 800px;
                margin: 0 auto;
                background: #f9f9f9;
            }}
            h2 {{
                background: {cat_info['color']};
                color: white;
                padding: 15px;
                border-radius: 8px;
                margin: -20px -20px 20px -20px;
            }}
            pre {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                white-space: pre-wrap;
                line-height: 1.5;
                border: 1px solid #ddd;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .back-link {{
                display: inline-block;
                margin-bottom: 20px;
                color: {cat_info['color']};
                text-decoration: none;
                font-weight: bold;
            }}
            .back-link:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <a href="javascript:window.close()" class="back-link">← Fermer cette fenêtre</a>
        <h2>{cat_info['emoji']} {category} - 📅 {date_formatted}</h2>
        <p style="color: #666; font-size: 14px; margin-bottom: 20px;">
            Fichier: <code style="background: #f0f0f0; padding: 2px 6px; border-radius: 3px;">{filename}</code>
        </p>
        <pre>{content}</pre>
    </body>
    </html>
    """

@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files like CSS, JS, and other assets"""
    try:
        # Handle common static file extensions
        if filename.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.eot')):
            with open(filename, 'rb' if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico', '.woff', '.woff2', '.ttf', '.eot')) else 'r', encoding=None if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico', '.woff', '.woff2', '.ttf', '.eot')) else 'utf-8') as f:
                content = f.read()
                # Set appropriate content type
                if filename.endswith('.css'):
                    response = app.response_class(content, mimetype='text/css')
                elif filename.endswith('.js'):
                    response = app.response_class(content, mimetype='application/javascript')
                else:
                    response = app.response_class(content)
                return response
        else:
            # For other files, try to serve them
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
    except FileNotFoundError:
        return "File not found", 404
    except Exception as e:
        return f"Error serving file: {str(e)}", 500

@app.route('/categories')
def get_categories():
    return jsonify(load_categories())

@app.route('/add_category', methods=['POST'])
def add_category():
    data = request.json
    name = data.get('name', '').strip().lower()
    if not name:
        return jsonify({"error": "Nom invalide"}), 400

    # Validation de la longueur (19 caractères maximum)
    if len(name) > 19:
        return jsonify({"error": f"Le nom de la catégorie ne peut pas dépasser 19 caractères ({len(name)}/19)"}), 400
    
    # Générer une couleur aléatoire
    color = f"#{random.randint(0, 0xFFFFFF):06x}"
    
    # Choisir un emoji aléatoire dans la liste
    emoji = random.choice(EMOJIS)
    
    categories = load_categories()
    if any(c['name'] == name for c in categories):
        return jsonify({"error": "Catégorie existe déjà"}), 400
    new_category = {"name": name, "emoji": emoji, "color": color}
    categories.append(new_category)
    save_categories(categories)
    return jsonify(new_category)

@app.route('/open_folder/<category>')
def open_folder(category):
    """Ouvre le dossier de la catégorie dans l'Explorateur Windows"""
    import subprocess
    import platform
    import time

    if platform.system() != 'Windows':
        return jsonify({"error": "Cette fonctionnalité n'est disponible que sous Windows"}), 400

    # Vérifier que la catégorie existe
    categories = load_categories()
    if not any(c['name'] == category for c in categories):
        return jsonify({"error": "Catégorie introuvable"}), 404

    try:
        folder_path = os.path.join(os.getcwd(), category)
        os.makedirs(folder_path, exist_ok=True)

        print(f"Tentative d'ouverture du dossier: {folder_path}")

        # Solution pour forcer Chrome en arrière-plan
        try:
            import pyperclip
            pyperclip.copy(folder_path)
            print(f"Chemin copié dans le presse-papier: {folder_path}")
        except ImportError:
            print("pyperclip non disponible")
        
        # VERSION ULTRA-RAPIDE - Utiliser le script optimisé
        script_path = os.path.join(os.path.dirname(os.getcwd()), 'minimize_chrome_fast.bat')
        
        if os.path.exists(script_path):
            subprocess.Popen([script_path, folder_path], shell=True)
            print(f"Script ultra-rapide utilisé: {folder_path}")
        else:
            # Fallback rapide
            subprocess.Popen(['explorer', folder_path], shell=True)
            print(f"Explorateur ouvert (fallback): {folder_path}")
            
            # Minimiser Chrome en arrière-plan
            try:
                ps_command = 'Get-Process chrome -ErrorAction SilentlyContinue | ForEach-Object { $hwnd = $_.MainWindowHandle; if ($hwnd -ne [IntPtr]::Zero) { Add-Type -TypeDefinition "using System; using System.Runtime.InteropServices; public class Win32 { [DllImport(\\"user32.dll\\")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow); }"; [Win32]::ShowWindow($hwnd, 6) } }'
                subprocess.Popen(['powershell', '-WindowStyle', 'Hidden', '-Command', ps_command], shell=True)
                print(f"Chrome minimisé (fallback): {folder_path}")
            except Exception as ps_error:
                print(f"Minimisation Chrome échouée: {ps_error}")

        return jsonify({
            "status": "opened",
            "path": folder_path
        })

    except Exception as e:
        print(f"Erreur lors de l'ouverture du dossier: {str(e)}")
        return jsonify({"error": f"Erreur: {str(e)}"}), 500

@app.route('/erase_category/<category>', methods=['DELETE'])
def erase_category(category):
    """Supprime complètement une catégorie et tous ses fichiers"""
    import shutil
    
    # Vérifier que la catégorie existe
    categories = load_categories()
    category_exists = any(c['name'] == category for c in categories)
    
    if not category_exists:
        return jsonify({"error": "Catégorie introuvable"}), 404
    
    try:
        # Chemin du dossier de la catégorie
        folder_path = os.path.join(os.getcwd(), category)
        
        # Supprimer le dossier et tous ses fichiers
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"Dossier supprimé: {folder_path}")
        
        # Supprimer la catégorie de la liste
        updated_categories = [c for c in categories if c['name'] != category]
        save_categories(updated_categories)
        
        return jsonify({
            "status": "deleted", 
            "category": category,
            "message": f"Catégorie '{category}' et tous ses fichiers ont été supprimés"
        })
        
    except Exception as e:
        print(f"Erreur lors de la suppression: {str(e)}")
        return jsonify({"error": f"Erreur lors de la suppression: {str(e)}"}), 500

@app.route('/backup_project', methods=['POST'])
def backup_project():
    """Crée un backup ZIP complet du projet avec la date"""
    try:
        # Obtenir la date actuelle
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        # Chemin du projet parent (G:\2brains)
        parent_dir = os.path.dirname(os.getcwd())
        
        # Nom du fichier de backup
        backup_filename = f"backup_2brains_{date_str}.zip"
        backup_path = os.path.join(parent_dir, backup_filename)
        
        print(f"Création du backup: {backup_path}")
        
        # Créer le fichier ZIP
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Parcourir tous les fichiers et dossiers du projet
            for root, dirs, files in os.walk(os.getcwd()):
                # Ignorer certains dossiers/fichiers système
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
                
                for file in files:
                    # Ignorer certains fichiers
                    if not file.startswith('.') and not file.endswith('.pyc'):
                        file_path = os.path.join(root, file)
                        # Chemin relatif dans le ZIP
                        arcname = os.path.relpath(file_path, os.getcwd())
                        zipf.write(file_path, arcname)
                        print(f"Ajouté au backup: {arcname}")
        
        # Vérifier que le fichier a été créé
        if os.path.exists(backup_path):
            file_size = os.path.getsize(backup_path)
            file_size_mb = round(file_size / (1024 * 1024), 2)
            
            return jsonify({
                "status": "success",
                "message": f"Backup créé avec succès !",
                "filename": backup_filename,
                "path": backup_path,
                "size_mb": file_size_mb,
                "date": date_str
            })
        else:
            return jsonify({"error": "Erreur lors de la création du fichier de backup"}), 500
            
    except Exception as e:
        print(f"Erreur lors de la création du backup: {str(e)}")
        return jsonify({"error": f"Erreur lors de la création du backup: {str(e)}"}), 500

def extract_file_creation_hour(category_name, filename):
    """Extrait l'heure de création la plus récente du fichier en lisant tout le contenu"""
    try:
        filepath = f"{category_name}/{filename}"
        if not os.path.exists(filepath):
            return None
            
        # Essayer différents encodages pour lire le fichier
        encodings_to_try = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
        
        for encoding in encodings_to_try:
            try:
                with open(filepath, "r", encoding=encoding) as f:
                    lines = f.readlines()
                    
                # Extraire toutes les heures du fichier
                hours = []
                for line in lines:
                    line = line.strip()
                    if line and ':' in line:
                        # Vérifier si la ligne commence par une heure (HH:MM:SS:)
                        parts = line.split(':')
                        if len(parts) >= 3:
                            try:
                                # Vérifier si les 3 premières parties sont des nombres
                                hour = int(parts[0])
                                minute = int(parts[1])
                                second = int(parts[2])
                                
                                # Vérifier que c'est une heure valide
                                if 0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59:
                                    hour_str = f"{hour:02d}:{minute:02d}:{second:02d}"
                                    hours.append(hour_str)
                            except ValueError:
                                continue
                
                # Retourner l'heure la plus récente
                if hours:
                    # Trier les heures et retourner la plus récente
                    hours.sort(reverse=True)
                    return hours[0]
                
                break
            except UnicodeDecodeError:
                continue
                
        return None
    except Exception as e:
        print(f"Erreur lors de l'extraction de l'heure pour {filename}: {e}")
        return None

@app.route('/search_files')
def search_files():
    """API de recherche de texte dans les fichiers"""
    try:
        import os
        import re
        from datetime import datetime

        search_term = request.args.get('q', '').strip()
        if not search_term:
            return jsonify({"success": False, "error": "Terme de recherche manquant"})

        # Configuration de la recherche
        root_dir = './'
        exclude_dirs = ['node_modules', '.git', '__pycache__', 'backups', '__pycache__']
        supported_extensions = ['.txt', '.md', '.js', '.py', '.html', '.css', '.json']

        results = []
        search_term_lower = search_term.lower()

        def search_in_file(filepath):
            """Recherche dans un fichier spécifique"""
            try:
                # Essayer différents encodages
                encodings_to_try = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
                content = None

                for encoding in encodings_to_try:
                    try:
                        with open(filepath, 'r', encoding=encoding) as f:
                            content = f.read()
                        break
                    except UnicodeDecodeError:
                        continue

                if content is None:
                    return None

                content_lower = content.lower()
                lines = content.split('\n')
                matches = []

                for line_num, line in enumerate(lines, 1):
                    if search_term_lower in line.lower():
                        # Extraire le contexte autour de la correspondance
                        context_start = max(0, line_num - 3)
                        context_end = min(len(lines), line_num + 3)
                        context_lines = lines[context_start:context_end]

                        matches.append({
                            'lineNumber': line_num,
                            'line': line.strip(),
                            'context': '\n'.join(context_lines),
                            'contextStart': context_start + 1,
                            'contextEnd': context_end
                        })

                if matches:
                    return {
                        'filePath': filepath,
                        'relativePath': os.path.relpath(filepath, root_dir),
                        'fileName': os.path.basename(filepath),
                        'directory': os.path.dirname(filepath),
                        'matches': matches,
                        'totalMatches': len(matches),
                        'fileSize': len(content)
                    }
            except Exception as e:
                print(f"Erreur lors de la lecture de {filepath}: {e}")
                return None

            return None

        def walk_directory(dir_path):
            """Parcourir récursivement un répertoire"""
            try:
                for item in os.listdir(dir_path):
                    if item.startswith('.'):
                        continue

                    full_path = os.path.join(dir_path, item)

                    if os.path.isdir(full_path):
                        if item not in exclude_dirs:
                            walk_directory(full_path)
                    else:
                        ext = os.path.splitext(item)[1].lower()
                        if ext in supported_extensions:
                            result = search_in_file(full_path)
                            if result:
                                results.append(result)
            except PermissionError:
                pass  # Ignorer les répertoires sans permission

        # Lancer la recherche
        walk_directory(root_dir)

        # Trier par nombre de correspondances (plus pertinentes en premier)
        results.sort(key=lambda x: x['totalMatches'], reverse=True)

        return jsonify({
            "success": True,
            "query": search_term,
            "totalFiles": len(results),
            "results": results[:100]  # Limiter à 100 résultats maximum
        })

    except Exception as e:
        print(f"Erreur lors de la recherche: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/all_notes')
def all_notes():
    """Retourne tous les fichiers de toutes les catégories dans une page dédiée avec système d'accordéon professionnel"""
    all_files_data = _get_all_files_cached()
    
    # Trier les fichiers par date décroissante
    all_files_data.sort(key=lambda x: x['date'], reverse=True)

    # Séparer les fichiers par catégorie et extraire l'heure de création
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
                'latest_file_hour': None  # Heure du fichier le plus récent
            }
        
        # Extraire l'heure de création du fichier
        file_hour = extract_file_creation_hour(category_name, item['filename'])
        
        categories_data[category_name]['files'].append({
            'filename': item['filename'],
            'date': item['date'],
            'hour': file_hour
        })
        
        # Mettre à jour la date et l'heure du fichier le plus récent si nécessaire
        if item['date'] > categories_data[category_name]['latest_file_date']:
            categories_data[category_name]['latest_file_date'] = item['date']
            categories_data[category_name]['latest_file_hour'] = file_hour
        elif item['date'] == categories_data[category_name]['latest_file_date'] and file_hour:
            # Si même date, prendre l'heure la plus récente
            current_hour = categories_data[category_name]['latest_file_hour']
            if not current_hour or file_hour > current_hour:
                categories_data[category_name]['latest_file_hour'] = file_hour

    # Trier les catégories par l'heure de création du fichier le plus récent (du plus récent au plus ancien)
    # Créer une clé de tri combinant date et heure
    def sort_key(category_item):
        cat_name, cat_data = category_item
        date = cat_data['latest_file_date']
        hour = cat_data['latest_file_hour'] or '00:00:00'
        # Créer une clé de tri: YYYY-MM-DD HH:MM:SS
        return f"{date} {hour}"
    
    sorted_categories = sorted(categories_data.items(), 
                             key=sort_key, 
                             reverse=True)

    # Générer le HTML pour chaque catégorie avec système d'accordéon (triées par date du fichier le plus récent)
    categories_html = ""
    for i, (cat_name, cat_data) in enumerate(sorted_categories):
        files_html = ""
        for file in cat_data['files']:
            date_formatted = file['date'].split('-')
            if len(date_formatted) == 3:
                date_formatted = f"{date_formatted[2]}/{date_formatted[1]}/{date_formatted[0]}"
            else:
                date_formatted = file['date']
            
            files_html += f"""
            <div class="file-item">
                <div class="file-info">
                    <span class="file-emoji">📄</span>
                    <span class="file-name">{file['filename'].replace(f"{cat_name}_", '').replace('.txt', '')}</span>
                    <span class="file-date">📅 {date_formatted}</span>
                </div>
                <div class="file-actions">
                    <a href="/read/{cat_name}/{file['filename']}" target="_blank" class="read-btn">📖 Lire</a>
                </div>
            </div>
            """
        
        # Formater la date et l'heure du fichier le plus récent
        latest_date_formatted = cat_data['latest_file_date'].split('-')
        if len(latest_date_formatted) == 3:
            latest_date_display = f"{latest_date_formatted[2]}/{latest_date_formatted[1]}/{latest_date_formatted[0]}"
        else:
            latest_date_display = cat_data['latest_file_date']
        
        # Ajouter l'heure si disponible
        latest_hour_display = ""
        if cat_data['latest_file_hour']:
            latest_hour_display = f" à {cat_data['latest_file_hour']}"
        
        categories_html += f"""
        <div class="accordion-item">
            <div class="accordion-header" onclick="toggleAccordion('category-{i}')">
                <div class="folder-info">
                    <span class="folder-emoji">{cat_data['emoji']}</span>
                    <span class="folder-name">{cat_name}</span>
                    <span class="file-count">({len(cat_data['files'])} fichiers)</span>
                    <span class="latest-date">🕐 Dernier: {latest_date_display}{latest_hour_display}</span>
                </div>
                <div class="accordion-icon" id="icon-category-{i}">▼</div>
            </div>
            <div class="accordion-content" id="category-{i}">
                <div class="files-container">
                    {files_html}
                </div>
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📚 Toutes les Notes - Navigation Hiérarchique</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: #000000;
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #6A4C93 0%, #8B5FBF 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5rem;
                margin-bottom: 10px;
                font-weight: 700;
            }}
            
            .header p {{
                opacity: 0.9;
                font-size: 1.1rem;
            }}
            
            .back-link {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 20px;
                color: white;
                text-decoration: none;
                font-weight: 600;
                padding: 12px 24px;
                background: rgba(255,255,255,0.2);
                border-radius: 50px;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            }}
            
            .back-link:hover {{
                background: rgba(255,255,255,0.3);
                transform: translateY(-2px);
            }}
            
            .search-container {{
                padding: 20px 30px;
                background: #f8f9fa;
                border-bottom: 1px solid #e9ecef;
            }}
            
            .search-box {{
                width: 100%;
                padding: 15px 20px;
                border: 2px solid #e9ecef;
                border-radius: 50px;
                font-size: 16px;
                transition: all 0.3s ease;
                background: white;
            }}
            
            .search-box:focus {{
                outline: none;
                border-color: #6A4C93;
                box-shadow: 0 0 0 3px rgba(106, 76, 147, 0.1);
            }}
            
            .accordion-container {{
                padding: 20px 30px;
            }}
            
            .accordion-item {{
                margin-bottom: 15px;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                transition: all 0.3s ease;
            }}
            
            .accordion-item:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }}
            
            .accordion-header {{
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 20px 25px;
                cursor: pointer;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: all 0.3s ease;
                border: none;
                width: 100%;
            }}
            
            .accordion-header:hover {{
                background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
            }}
            
            .folder-info {{
                display: flex;
                align-items: center;
                gap: 15px;
            }}
            
            .folder-emoji {{
                font-size: 2rem;
            }}
            
            .folder-name {{
                font-size: 1.3rem;
                font-weight: 600;
                color: #2c3e50;
            }}
            
            .file-count {{
                font-size: 0.9rem;
                color: #6c757d;
                background: rgba(108, 117, 125, 0.1);
                padding: 4px 12px;
                border-radius: 20px;
            }}
            
            .latest-date {{
                font-size: 0.8rem;
                color: #28a745;
                background: rgba(40, 167, 69, 0.1);
                padding: 4px 10px;
                border-radius: 15px;
                font-weight: 600;
            }}
            
            .accordion-icon {{
                font-size: 1.2rem;
                color: #6A4C93;
                transition: transform 0.3s ease;
                font-weight: bold;
            }}
            
            .accordion-content {{
                max-height: 0;
                overflow: hidden;
                transition: max-height 0.4s ease-out;
                background: white;
            }}
            
            .accordion-content.active {{
                max-height: 1000px;
                transition: max-height 0.4s ease-in;
            }}
            
            .files-container {{
                padding: 20px 25px;
                max-height: 400px;
                overflow-y: auto;
                scrollbar-width: thin;
                scrollbar-color: #6A4C93 #f1f1f1;
            }}
            
            .files-container::-webkit-scrollbar {{
                width: 8px;
            }}
            
            .files-container::-webkit-scrollbar-track {{
                background: #f1f1f1;
                border-radius: 10px;
            }}
            
            .files-container::-webkit-scrollbar-thumb {{
                background: #6A4C93;
                border-radius: 10px;
            }}
            
            .files-container::-webkit-scrollbar-thumb:hover {{
                background: #5a3d7a;
            }}
            
            .file-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                margin-bottom: 10px;
                background: #f8f9fa;
                border-radius: 12px;
                transition: all 0.3s ease;
                border-left: 4px solid transparent;
            }}
            
            .file-item:hover {{
                background: #e3f2fd;
                border-left-color: #6A4C93;
                transform: translateX(5px);
            }}
            
            .file-info {{
                display: flex;
                align-items: center;
                gap: 15px;
                flex: 1;
            }}
            
            .file-emoji {{
                font-size: 1.5rem;
            }}
            
            .file-name {{
                font-weight: 600;
                color: #2c3e50;
                font-size: 1.1rem;
            }}
            
            .file-date {{
                font-size: 0.9rem;
                color: #6c757d;
                background: rgba(108, 117, 125, 0.1);
                padding: 4px 10px;
                border-radius: 15px;
            }}
            
            .read-btn {{
                background: linear-gradient(135deg, #6A4C93 0%, #8B5FBF 100%);
                color: white;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 25px;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(106, 76, 147, 0.3);
            }}
            
            .read-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(106, 76, 147, 0.4);
            }}
            
            .empty-state {{
                text-align: center;
                padding: 60px 20px;
                color: #6c757d;
            }}
            
            .empty-state .emoji {{
                font-size: 4rem;
                margin-bottom: 20px;
            }}
            
            .empty-state h3 {{
                font-size: 1.5rem;
                margin-bottom: 10px;
                color: #495057;
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    margin: 10px;
                    border-radius: 15px;
                }}
                
                .header {{
                    padding: 20px;
                }}
                
                .header h1 {{
                    font-size: 2rem;
                }}
                
                .search-container, .accordion-container {{
                    padding: 15px 20px;
                }}
                
                .accordion-header {{
                    padding: 15px 20px;
                }}
                
                .folder-name {{
                    font-size: 1.1rem;
                }}
                
                .file-item {{
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 10px;
                }}
                
                .file-info {{
                    width: 100%;
                }}
                
                .read-btn {{
                    align-self: flex-end;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <a href="javascript:window.close()" class="back-link">
                    ← Retour à l'accueil
                </a>
                <h1>📚 Toutes les Notes</h1>
                <p>Navigation hiérarchique professionnelle</p>
            </div>
            
            <div class="search-container">
                <input type="text" class="search-box" placeholder="🔍 Rechercher dans les fichiers..." id="searchInput">
            </div>
            
            <div class="accordion-container">
                {categories_html or '<div class="empty-state"><div class="emoji">📁</div><h3>Aucune note trouvée</h3><p>Commencez par créer des notes dans vos catégories.</p></div>'}
            </div>
        </div>
        
        <script></script>
    </body>
    </html>
    """


@app.route('/fusion/global', methods=['POST'])
def fusion_global():
    """Fusionne toutes les notes de toutes les catégories en un seul fichier"""
    try:
        # Créer le dossier fusion_global s'il n'existe pas
        fusion_dir = "fusion_global"
        if not os.path.exists(fusion_dir):
            os.makedirs(fusion_dir)
        
        # Récupérer tous les fichiers
        all_files_data = _get_all_files_cached()
        
        # Trier par date et heure
        all_files_data.sort(key=lambda x: (x['date'], x.get('hour', '00:00:00')), reverse=True)
        
        # Créer le nom du fichier fusionné avec timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fusion_filename = f"fusion_globale_{timestamp}.txt"
        fusion_filepath = os.path.join(fusion_dir, fusion_filename)
        
        # Fusionner tous les fichiers
        with open(fusion_filepath, 'w', encoding='utf-8') as fusion_file:
            fusion_file.write("=" * 80 + "\n")
            fusion_file.write("🔗 FUSION GLOBALE DE TOUTES LES NOTES\n")
            fusion_file.write("=" * 80 + "\n")
            fusion_file.write(f"📅 Date de fusion: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
            fusion_file.write(f"📊 Nombre total de fichiers: {len(all_files_data)}\n")
            fusion_file.write("=" * 80 + "\n\n")
            
            current_category = None
            for file_data in all_files_data:
                category_name = file_data['category']
                filename = file_data['filename']
                file_date = file_data['date']
                
                # Ajouter un séparateur de catégorie si nécessaire
                if current_category != category_name:
                    if current_category is not None:
                        fusion_file.write("\n" + "=" * 80 + "\n\n")
                    fusion_file.write(f"📁 CATÉGORIE: {category_name.upper()}\n")
                    fusion_file.write("-" * 40 + "\n\n")
                    current_category = category_name
                
                # Lire et ajouter le contenu du fichier
                filepath = f"{category_name}/{filename}"
                if os.path.exists(filepath):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                            if content:
                                fusion_file.write(f"📄 {filename} ({file_date})\n")
                                fusion_file.write("-" * 30 + "\n")
                                fusion_file.write(content)
                                fusion_file.write("\n\n")
                    except Exception as e:
                        print(f"Erreur lors de la lecture de {filepath}: {e}")
                        fusion_file.write(f"❌ Erreur lors de la lecture de {filename}\n\n")
        
        return jsonify({
            "success": True,
            "message": f"Fusion globale réussie ! Fichier créé: {fusion_filename}",
            "filename": fusion_filename,
            "filepath": fusion_filepath,
            "total_files": len(all_files_data)
        })
        
    except Exception as e:
        print(f"Erreur lors de la fusion globale: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/fusion/category', methods=['POST'])
def fusion_category():
    """Fusionne les notes des catégories sélectionnées"""
    try:
        data = request.get_json()
        selected_categories = data.get('categories', [])
        
        if not selected_categories:
            return jsonify({"success": False, "error": "Aucune catégorie sélectionnée"}), 400
        
        # Créer le dossier fusion_global s'il n'existe pas
        fusion_dir = "fusion_global"
        if not os.path.exists(fusion_dir):
            os.makedirs(fusion_dir)
        
        # Récupérer tous les fichiers
        all_files_data = _get_all_files_cached()
        
        # Filtrer les fichiers des catégories sélectionnées
        filtered_files = [f for f in all_files_data if f['category'] in selected_categories]
        
        if not filtered_files:
            return jsonify({"success": False, "error": "Aucun fichier trouvé dans les catégories sélectionnées"}), 400
        
        # Trier par date et heure
        filtered_files.sort(key=lambda x: (x['date'], x.get('hour', '00:00:00')), reverse=True)
        
        # Créer le nom du fichier fusionné avec timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        categories_str = "_".join(selected_categories[:3])  # Limiter la longueur du nom
        if len(selected_categories) > 3:
            categories_str += f"_et_{len(selected_categories)-3}_autres"
        fusion_filename = f"fusion_categories_{categories_str}_{timestamp}.txt"
        fusion_filepath = os.path.join(fusion_dir, fusion_filename)
        
        # Fusionner les fichiers sélectionnés
        with open(fusion_filepath, 'w', encoding='utf-8') as fusion_file:
            fusion_file.write("=" * 80 + "\n")
            fusion_file.write("📁 FUSION PAR CATÉGORIES\n")
            fusion_file.write("=" * 80 + "\n")
            fusion_file.write(f"📅 Date de fusion: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
            fusion_file.write(f"📊 Catégories sélectionnées: {', '.join(selected_categories)}\n")
            fusion_file.write(f"📊 Nombre total de fichiers: {len(filtered_files)}\n")
            fusion_file.write("=" * 80 + "\n\n")
            
            current_category = None
            for file_data in filtered_files:
                category_name = file_data['category']
                filename = file_data['filename']
                file_date = file_data['date']
                
                # Ajouter un séparateur de catégorie si nécessaire
                if current_category != category_name:
                    if current_category is not None:
                        fusion_file.write("\n" + "=" * 80 + "\n\n")
                    fusion_file.write(f"📁 CATÉGORIE: {category_name.upper()}\n")
                    fusion_file.write("-" * 40 + "\n\n")
                    current_category = category_name
                
                # Lire et ajouter le contenu du fichier
                filepath = f"{category_name}/{filename}"
                if os.path.exists(filepath):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                            if content:
                                fusion_file.write(f"📄 {filename} ({file_date})\n")
                                fusion_file.write("-" * 30 + "\n")
                                fusion_file.write(content)
                                fusion_file.write("\n\n")
                    except Exception as e:
                        print(f"Erreur lors de la lecture de {filepath}: {e}")
                        fusion_file.write(f"❌ Erreur lors de la lecture de {filename}\n\n")
        
        return jsonify({
            "success": True,
            "message": f"Fusion par catégories réussie ! Fichier créé: {fusion_filename}",
            "filename": fusion_filename,
            "filepath": fusion_filepath,
            "categories": selected_categories,
            "total_files": len(filtered_files)
        })
        
    except Exception as e:
        print(f"Erreur lors de la fusion par catégories: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/fusion/single-category', methods=['POST'])
def fusion_single_category():
    """Fusionne tous les fichiers d'une seule catégorie"""
    try:
        data = request.get_json()
        category_name = data.get('category')
        
        if not category_name:
            return jsonify({"success": False, "error": "Nom de catégorie manquant"}), 400
        
        # Créer le dossier fusion_global s'il n'existe pas
        fusion_dir = "fusion_global"
        if not os.path.exists(fusion_dir):
            os.makedirs(fusion_dir)
        
        # Récupérer tous les fichiers
        all_files_data = _get_all_files_cached()
        
        # Filtrer les fichiers de la catégorie spécifique
        category_files = [f for f in all_files_data if f['category'] == category_name]
        
        if not category_files:
            return jsonify({"success": False, "error": f"Aucun fichier trouvé dans la catégorie '{category_name}'"}), 400
        
        # Trier par date et heure
        category_files.sort(key=lambda x: (x['date'], x.get('hour', '00:00:00')), reverse=True)
        
        # Créer le nom du fichier fusionné avec timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fusion_filename = f"fusion_{category_name}_{timestamp}.txt"
        fusion_filepath = os.path.join(fusion_dir, fusion_filename)
        
        # Fusionner les fichiers de la catégorie
        with open(fusion_filepath, 'w', encoding='utf-8') as fusion_file:
            fusion_file.write("=" * 80 + "\n")
            fusion_file.write(f"📁 FUSION DE LA CATÉGORIE: {category_name.upper()}\n")
            fusion_file.write("=" * 80 + "\n")
            fusion_file.write(f"📅 Date de fusion: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
            fusion_file.write(f"📊 Catégorie: {category_name}\n")
            fusion_file.write(f"📊 Nombre total de fichiers: {len(category_files)}\n")
            fusion_file.write("=" * 80 + "\n\n")
            
            for file_data in category_files:
                filename = file_data['filename']
                file_date = file_data['date']
                
                # Lire et ajouter le contenu du fichier
                filepath = f"{category_name}/{filename}"
                if os.path.exists(filepath):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                            if content:
                                fusion_file.write(f"📄 {filename} ({file_date})\n")
                                fusion_file.write("-" * 30 + "\n")
                                fusion_file.write(content)
                                fusion_file.write("\n\n")
                    except Exception as e:
                        print(f"Erreur lors de la lecture de {filepath}: {e}")
                        fusion_file.write(f"❌ Erreur lors de la lecture de {filename}\n\n")
        
        return jsonify({
            "success": True,
            "message": f"Fusion de la catégorie '{category_name}' réussie ! Fichier créé: {fusion_filename}",
            "filename": fusion_filename,
            "filepath": fusion_filepath,
            "category": category_name,
            "total_files": len(category_files)
        })
        
    except Exception as e:
        print(f"Erreur lors de la fusion de la catégorie: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    import os
    # Only run in debug mode if explicitly set via environment variable
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5008)))