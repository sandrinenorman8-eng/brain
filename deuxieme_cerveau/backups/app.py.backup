from flask import Flask, request, jsonify, abort, send_from_directory, make_response
import os
import re
from datetime import datetime
import json
import random
import zipfile
import shutil
from functools import lru_cache
from werkzeug.utils import secure_filename
from category_path_resolver import get_category_path, get_absolute_category_path

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
    # Utiliser le resolver pour obtenir le bon chemin hiérarchique
    category_path = get_category_path(category)
    os.makedirs(category_path, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    # Utiliser le nom de la catégorie au lieu de "notes" pour une meilleure organisation
    filename = os.path.join(category_path, f"{category}_{date_str}.txt")
    with open(filename, "a", encoding='utf-8') as f:
        time_str = datetime.now().strftime("%H:%M:%S")
        f.write(f"{time_str}: {data}\n")
    # Invalider le cache des fichiers
    _get_all_files_cached.cache_clear()
    return jsonify({"status": "saved"})

@app.route('/list/<category>')
def list_files(category):
    # Utiliser le resolver pour obtenir le bon chemin hiérarchique
    category_path = get_category_path(category)
    if not os.path.exists(category_path):
        return jsonify([])
    # Chercher les fichiers qui commencent par le nom de la catégorie
    files = [f for f in os.listdir(category_path)
            if f.startswith(f'{category}_') and f.endswith('.txt')]
    files.sort(reverse=True)
    return jsonify(files)

@lru_cache(maxsize=1)
def _get_all_files_cached():
    """Version cachée de all_files pour optimiser les performances"""
    categories = load_categories()
    all_files_data = []

    for cat in categories:
        category_path = get_category_path(cat['name'])
        if os.path.exists(category_path):
            # Chercher les fichiers qui commencent par le nom de la catégorie
            files = [f for f in os.listdir(category_path)
                    if f.startswith(f"{cat['name']}_") and f.endswith('.txt')]
            for file in files:
                # Extraire l'heure de création du fichier
                file_hour = extract_file_creation_hour(cat['name'], file)

                all_files_data.append({
                    'category': cat['name'],
                    'emoji': cat['emoji'],
                    'color': cat['color'],
                    'filename': file,
                    'date': file.replace(f"{cat['name']}_", '').replace('.txt', ''),
                    'hour': file_hour or '00:00:00'
                })

    # Trier par date ET heure décroissantes (les plus récents en premier)
    all_files_data.sort(key=lambda x: (x['date'], x['hour']), reverse=True)
    return all_files_data

@app.route('/all_files')
def all_files():
    """Retourne tous les fichiers de toutes les catégories (optimisé avec cache)"""
    return jsonify(_get_all_files_cached())

@app.route('/read/<category>/<filename>')
def read_file(category, filename):
    # 1. Decode URL-encoded parameters
    import urllib.parse
    category = urllib.parse.unquote(category)
    filename = urllib.parse.unquote(filename)
    
    # 2. Define the absolute path for the application's root
    app_root = os.path.abspath(os.path.dirname(__file__))

    # 3. Define the absolute path for the intended category directory using resolver
    category_dir = get_absolute_category_path(category)

    # 4. Construct the final, full file path - use original filename to preserve accented characters
    filepath = os.path.join(category_dir, filename)

    # 5. CRITICAL: Verify the final path is within the allowed directory
    if not filepath.startswith(category_dir):
        abort(400, "Unauthorized file access attempt.")

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
@app.route('/index.html')
def index():
    # Serve index.html safely from current directory
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        return f"Error serving index.html: {e}", 500

@app.route('/test_open_folder.html')
def test_open_folder_page():
    # Serve test page for open_folder functionality
    try:
        return send_from_directory('.', 'test_open_folder.html')
    except Exception as e:
        return f"Error serving test page: {e}", 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    # Serve static files from the static directory
    return send_from_directory('static', filename)

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

    # Invalider le cache des fichiers après création d'une nouvelle catégorie
    _get_all_files_cached.cache_clear()
    print(f"Cache invalide apres creation de la categorie '{name}'")

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
        folder_path = get_absolute_category_path(category)
        os.makedirs(folder_path, exist_ok=True)
        
        # Normaliser le chemin pour Windows (remplacer / par \)
        folder_path_normalized = os.path.normpath(folder_path)

        print(f"Tentative d'ouverture du dossier: {folder_path_normalized}")

        # Ouvrir l'explorateur Windows avec le chemin normalisé
        # Utiliser os.startfile qui est la méthode recommandée pour Windows
        try:
            os.startfile(folder_path_normalized)
            print(f"✅ Dossier ouvert avec os.startfile: {folder_path_normalized}")
        except Exception as startfile_error:
            print(f"❌ os.startfile échoué: {startfile_error}")
            # Fallback: utiliser explorer.exe avec chemin entre guillemets
            try:
                subprocess.Popen(f'explorer "{folder_path_normalized}"', shell=True)
                print(f"✅ Dossier ouvert avec explorer (fallback): {folder_path_normalized}")
            except Exception as explorer_error:
                print(f"❌ explorer fallback échoué: {explorer_error}")
                raise

        return jsonify({
            "status": "opened",
            "path": folder_path_normalized
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
        # Chemin du dossier de la catégorie using resolver
        folder_path = get_absolute_category_path(category)
        
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

@app.route('/upload_file', methods=['POST'])
def upload_file():
    """Upload a file to a selected category directory"""
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier fourni"}), 400
        
        file = request.files['file']
        category = request.form.get('category', '').strip()
        
        # Validate inputs
        if file.filename == '':
            return jsonify({"error": "Nom de fichier vide"}), 400
        
        if not category:
            return jsonify({"error": "Catégorie non spécifiée"}), 400
        
        # Verify category exists
        categories = load_categories()
        if not any(c['name'] == category for c in categories):
            return jsonify({"error": "Catégorie invalide"}), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({"error": "Nom de fichier invalide"}), 400
        
        # Create category directory if it doesn't exist using resolver
        category_path = get_category_path(category)
        os.makedirs(category_path, exist_ok=True)
        
        # Check if file already exists and create unique name if needed
        filepath = os.path.join(category_path, filename)
        if os.path.exists(filepath):
            name, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(filepath):
                filename = f"{name}_{counter}{ext}"
                filepath = os.path.join(category_path, filename)
                counter += 1
        
        # Save the file
        file.save(filepath)
        
        # Get file size
        file_size = os.path.getsize(filepath)
        file_size_kb = round(file_size / 1024, 2)
        
        # Invalidate cache
        _get_all_files_cached.cache_clear()
        
        print(f"✅ File uploaded: {filepath} ({file_size_kb} KB)")
        
        return jsonify({
            "status": "success",
            "message": "Fichier téléchargé avec succès",
            "filename": filename,
            "category": category,
            "path": filepath,
            "size_kb": file_size_kb
        })
        
    except Exception as e:
        print(f"❌ Error uploading file: {str(e)}")
        return jsonify({"error": f"Erreur lors du téléchargement: {str(e)}"}), 500

@app.route('/backup_project', methods=['POST'])
def backup_project():
    """Crée un backup ZIP complet de TOUT le dossier memobrik (G:\memobrik)"""
    try:
        # Obtenir la date actuelle
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        # Chemin du dossier memobrik (parent de deuxieme_cerveau)
        memobrik_dir = os.path.dirname(os.getcwd())
        
        # Nom du fichier de backup
        backup_filename = f"backup_memobrik_complet_{date_str}.zip"
        backup_path = os.path.join(memobrik_dir, backup_filename)
        
        print(f"Création du backup COMPLET de: {memobrik_dir}")
        print(f"Destination: {backup_path}")
        
        # Dossier de destination des backups
        zip_dir = os.path.join(memobrik_dir, 'zip')
        os.makedirs(zip_dir, exist_ok=True)
        
        # Nouveau chemin du backup dans le dossier zip/
        backup_path = os.path.join(zip_dir, backup_filename)
        
        print(f"Destination backup: {backup_path}")
        
        # Créer le fichier ZIP
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Parcourir TOUT le dossier memobrik
            for root, dirs, files in os.walk(memobrik_dir):
                # Ignorer certains dossiers/fichiers système et le dossier zip/
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and d != 'node_modules' and d != 'zip']
                
                for file in files:
                    # Ignorer certains fichiers
                    if not file.startswith('.') and not file.endswith('.pyc'):
                        file_path = os.path.join(root, file)
                        # Chemin relatif dans le ZIP (depuis memobrik)
                        arcname = os.path.relpath(file_path, memobrik_dir)
                        zipf.write(file_path, arcname)
                        print(f"Ajouté: {arcname}")
        
        # Vérifier que le fichier a été créé
        if os.path.exists(backup_path):
            file_size = os.path.getsize(backup_path)
            file_size_mb = round(file_size / (1024 * 1024), 2)
            
            return jsonify({
                "status": "success",
                "message": f"Backup COMPLET créé avec succès !",
                "filename": backup_filename,
                "path": backup_path,
                "size_mb": file_size_mb,
                "date": date_str,
                "scope": "TOUT le dossier memobrik (G:\\memobrik)"
            })
        else:
            return jsonify({"error": "Erreur lors de la création du fichier de backup"}), 500
            
    except Exception as e:
        print(f"Erreur lors de la création du backup: {str(e)}")
        return jsonify({"error": f"Erreur lors de la création du backup: {str(e)}"}), 500

def extract_file_creation_hour(category_name, filename):
    """Extrait l'heure de création la plus récente du fichier en lisant tout le contenu"""
    try:
        category_path = get_category_path(category_name)
        filepath = os.path.join(category_path, filename)
        if not os.path.exists(filepath):
            return None

        # Try different encodings (UTF-8 first, then others)
        encodings_to_try = ['utf-8', 'utf-8-sig', 'cp1252', 'latin-1', 'iso-8859-1']

        for encoding in encodings_to_try:
            try:
                with open(filepath, "r", encoding=encoding) as f:
                    lines = f.read().splitlines()  # Read all lines at once
                # Replace problematic characters
                lines = [line.replace('�', 'é').replace('�', 'à').replace('�', 'â')
                        .replace('�', 'ê').replace('�', 'î').replace('�', 'ô')
                        .replace('�', 'û').replace('�', 'ç').replace('�', 'ë')
                        .replace('�', 'ï').replace('�', 'ü') for line in lines]
                break

            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Warning: Error reading {filepath} with {encoding}: {e}")
                continue

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

        return None
    except Exception as e:
        print(f"Erreur lors de l'extraction de l'heure pour {filename}: {e}")
        return None

@app.route('/all_notes')
def all_notes():
    """Sert la page standalone avec barre de recherche fonctionnelle."""
    try:
        return send_from_directory('.', 'all_notes_standalone.html')
    except Exception as e:
        return f"Erreur lors du chargement de la page: {e}", 500

@app.route('/all_notes_data')
def all_notes_data():
    """API endpoint pour fournir les données des notes au format JSON"""
    try:
        all_files_data = _get_all_files_cached()
        
        # Séparer les fichiers par catégorie
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
            
            # Extraire l'heure de création du fichier
            file_hour = extract_file_creation_hour(category_name, item['filename'])
            
            categories_data[category_name]['files'].append({
                'filename': item['filename'],
                'date': item['date'],
                'hour': file_hour
            })

            # Mettre à jour la date et l'heure du fichier le plus récent
            current_latest_date = categories_data[category_name]['latest_file_date']
            if item['date'] > current_latest_date:
                categories_data[category_name]['latest_file_date'] = item['date']
                categories_data[category_name]['latest_file_hour'] = file_hour or '00:00:00'
            elif item['date'] == current_latest_date:
                # Même date, comparer les heures
                current_hour = categories_data[category_name].get('latest_file_hour', '00:00:00')
                if (file_hour or '00:00:00') > current_hour:
                    categories_data[category_name]['latest_file_hour'] = file_hour or '00:00:00'
            # Initialiser latest_file_hour si pas encore défini
            if 'latest_file_hour' not in categories_data[category_name]:
                categories_data[category_name]['latest_file_hour'] = file_hour or '00:00:00'

        # Trier les catégories par date et heure du fichier le plus récent
        sorted_categories = sorted(categories_data.items(),
                                 key=lambda x: (x[1]['latest_file_date'], x[1].get('latest_file_hour', '00:00:00')),
                                 reverse=True)

        # Générer le HTML pour chaque catégorie
        categories_html = ""
        for i, (cat_name, cat_data) in enumerate(sorted_categories):
            files_html = ""
            for file in cat_data['files']:
                date_formatted = file['date'].split('-')
                if len(date_formatted) == 3:
                    date_formatted = f"{date_formatted[2]}/{date_formatted[1]}/{date_formatted[0]}"
                else:
                    date_formatted = file['date']
                
                # Afficher la date et l'heure si disponible
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
                    <a href="/read/{cat_name}/{file['filename']}" target="_blank" class="read-btn">Lire</a>
                </div>
                """
            
            # Formater la date du fichier le plus récent
            latest_date_formatted = cat_data['latest_file_date'].split('-')
            if len(latest_date_formatted) == 3:
                latest_date_display = f"{latest_date_formatted[2]}/{latest_date_formatted[1]}/{latest_date_formatted[0]}"
                # Ajouter l'heure si disponible
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

@app.route('/search_content', methods=['POST'])
def search_content():
    """API endpoint pour la recherche de contenu - proxy vers le serveur Node.js"""
    try:
        import requests
        
        # Récupérer le terme de recherche
        data = request.get_json()
        search_term = data.get('term', '')
        
        if not search_term:
            return jsonify({'error': 'Terme de recherche manquant'}), 400
        
        # Faire appel au serveur Node.js de recherche
        try:
            response = requests.post('http://localhost:3008/search', 
                                   json={'term': search_term},
                                   timeout=10)
            
            if response.status_code == 200:
                return jsonify(response.json())
            else:
                return jsonify({'error': f'Erreur serveur de recherche: {response.status_code}'}), 500
                
        except requests.exceptions.ConnectionError:
            return jsonify({'error': 'Serveur de recherche non disponible. Démarrez-le avec: node search-server.js'}), 503
        except requests.exceptions.Timeout:
            return jsonify({'error': 'Timeout du serveur de recherche'}), 504
        except Exception as e:
            return jsonify({'error': f'Erreur lors de la recherche: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Erreur interne: {str(e)}'}), 500

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
                
                # Lire et ajouter le contenu du fichier using resolver
                category_path = get_category_path(category_name)
                filepath = os.path.join(category_path, filename)
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
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"success": False, "error": "Données JSON invalides"}), 400
        selected_categories = data.get('categories', [])
        
        if not selected_categories:
            return jsonify({"success": False, "error": "Aucune catégorie sélectionnée"}), 400
        
        # Créer le dossier fusion_categories s'il n'existe pas
        fusion_dir = "fusion_categories"
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
                
                # Lire et ajouter le contenu du fichier using resolver
                category_path = get_category_path(category_name)
                filepath = os.path.join(category_path, filename)
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
        
        # Créer le dossier fusion_categories s'il n'existe pas
        fusion_dir = "fusion_categories"
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
                
                # Lire et ajouter le contenu du fichier using resolver
                category_path = get_category_path(category_name)
                filepath = os.path.join(category_path, filename)
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

def create_date_pattern():
    """Create a comprehensive regex pattern for date detection (same as journal_viewer.py)"""
    patterns = [
        r'\b\d{4}-\d{2}-\d{2}\b',  # ISO format: YYYY-MM-DD
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # US format: MM/DD/YYYY
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # European format: DD/MM/YYYY
        r'\b\d{1,2}-\d{1,2}-\d{4}\b',  # DD-MM-YYYY format
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Full month
        r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',  # DD Month YYYY
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b',  # Abbreviated month
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b'  # DD Month YYYY abbreviated
    ]
    return '|'.join(patterns)

def read_and_merge_files(folder_path):
    """Read all text files from folder and merge their content (same as journal_viewer.py)"""
    merged_content = []

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")

    # Get all text files that start with folder name
    folder_name = os.path.basename(folder_path)
    files = [f for f in os.listdir(folder_path)
            if f.startswith(f'{folder_name}_') and f.endswith('.txt')]

    if not files:
        return ""

    # Sort files by name (which contains dates)
    files.sort()

    # Read each file
    for filename in files:
        filepath = os.path.join(folder_path, filename)
        try:
            # Try different encodings (UTF-8 first, then others)
            encodings_to_try = ['utf-8', 'utf-8-sig', 'cp1252', 'latin-1', 'iso-8859-1']
            content = None

            for encoding in encodings_to_try:
                try:
                    with open(filepath, 'r', encoding=encoding) as file:
                        content = file.read()
                    # Replace problematic characters
                    content = content.replace('�', 'é')
                    content = content.replace('�', 'à')
                    content = content.replace('�', 'â')
                    content = content.replace('�', 'ê')
                    content = content.replace('�', 'î')
                    content = content.replace('�', 'ô')
                    content = content.replace('�', 'û')
                    content = content.replace('�', 'ç')
                    content = content.replace('�', 'ë')
                    content = content.replace('�', 'ï')
                    content = content.replace('�', 'ü')
                    break
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    print(f"Warning: Error reading {filepath} with {encoding}: {e}")
                    continue

            if content is None:
                content = "❌ Error reading file"

            if content.strip():  # Only add non-empty files
                # Add file header
                merged_content.append(f"\n{'='*50}")
                merged_content.append(f"FILE: {filename}")
                merged_content.append(f"{'='*50}\n")
                merged_content.append(content)
                merged_content.append("\n")

        except Exception as e:
            print(f"Warning: Could not read file {filepath}: {e}")
            continue

    return '\n'.join(merged_content)

def highlight_dates(content):
    """Highlight all dates in the content using regex replacement (same as journal_viewer.py)"""
    date_pattern = create_date_pattern()

    def replace_date(match):
        date_text = match.group(0)
        return f'<span style="color: #ff6b6b; font-weight: bold;">{date_text}</span>'

    # Apply highlighting
    highlighted_content = re.sub(date_pattern, replace_date, content, flags=re.IGNORECASE)
    return highlighted_content




def generate_html(content, title="Journal Viewer - Dark Mode"):
    """Generate HTML with dark mode styling (same as journal_viewer.py)"""
    html_template = """
<!DOCTYPE html>
<html class=\"dark\" lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{title}</title>
    <link href=\"https://fonts.googleapis.com\" rel=\"preconnect\"/>
    <link crossorigin=\"\" href=\"https://fonts.gstatic.com\" rel=\"preconnect\"/>
    <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&amp;display=swap\" rel=\"stylesheet\"/>
    <script src=\"https://cdn.tailwindcss.com?plugins=forms,container-queries\"></script>
    <script>
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            colors: {
              "primary": "#137fec",
              "background-light": "#f6f7f8",
              "background-dark": "#101922",
            },
            fontFamily: {
              "display": ["Inter"]
            },
            borderRadius: {
              "DEFAULT": "0.25rem",
              "lg": "0.5rem",
              "xl": "0.75rem",
              "full": "9999px"
            },
          },
        },
      }
    </script>
    <link href=\"https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined\" rel=\"stylesheet\"/>
</head>
<body class=\"font-display bg-background-light dark:bg-background-dark text-stone-800 dark:text-stone-200\">
  <div class=\"flex flex-col min-h-screen\">
    <header class=\"sticky top-0 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-sm z-10\">
      <div class=\"container mx-auto px-4 sm:px-6 lg:px-8\">
        <div class=\"flex items-center justify-between h-16 border-b border-stone-200 dark:border-stone-800\">
          <div class=\"flex items-center gap-4\">
            <div class=\"text-primary size-7\">
              <svg fill=\"none\" viewBox=\"0 0 48 48\" xmlns=\"http://www.w3.org/2000/svg\">
                <path d=\"M42.4379 44C42.4379 44 36.0744 33.9038 41.1692 24C46.8624 12.9336 42.2078 4 42.2078 4L7.01134 4C7.01134 4 11.6577 12.932 5.96912 23.9969C0.876273 33.9029 7.27094 44 7.27094 44L42.4379 44Z\" fill=\"currentColor\"></path>
              </svg>
                </div>
            <h1 class=\"text-xl font-bold text-stone-900 dark:text-white\">{title}</h1>
          </div>
        </div>
      </div>
    </header>

    <main class=\"flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-8\">
      <div class=\"max-w-4xl mx-auto\">
        <div class=\"bg-white dark:bg-stone-800 rounded-lg shadow-md border border-stone-200 dark:border-stone-700 p-6\">
          <div class=\"prose prose-stone dark:prose-invert max-w-none\" style=\"white-space: pre-wrap;\">{content}</div>
        </div>
      </div>
    </main>
            </div>
        </body>
        </html>
        """

    return html_template.replace("{content}", content).replace("{title}", title)

def fusion_files_from_folder(folder_path):
    """Main function to process files from folder (same logic as journal_viewer.py)"""
    try:
        # Read and merge all text files
        merged_content = read_and_merge_files(folder_path)

        if not merged_content.strip():
            return f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Aucun fichier trouvé</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #1a1a1a;
                        color: #e0e0e0;
                        padding: 20px;
                        text-align: center;
                    }}
                    .empty-container {{
                        max-width: 600px;
                        margin: 50px auto;
                        background-color: #2b2b2b;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                    }}
                    h1 {{ color: #81c784; }}
                    .back-link {{
                        display: inline-block;
                        margin-top: 20px;
                        color: #00f6ff;
                        text-decoration: none;
                    }}
                </style>
            </head>
            <body>
                <div class="empty-container">
                    <h1>📁 Dossier vide</h1>
                    <p>Le dossier "<strong>{os.path.basename(folder_path)}</strong>" ne contient pas de fichiers texte.</p>
                    <p><a href="javascript:window.close()" class="back-link">← Fermer cette fenêtre</a></p>
                </div>
            </body>
            </html>
            """

        # Highlight dates
        highlighted_content = highlight_dates(merged_content)

        # Generate HTML
        html_content = generate_html(highlighted_content)

        return html_content

    except Exception as e:
        return f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Erreur de fusion</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                    padding: 20px;
                    text-align: center;
                }}
                .error-container {{
                    max-width: 600px;
                    margin: 50px auto;
                    background-color: #2b2b2b;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                }}
                h1 {{ color: #ff6b6b; }}
                .back-link {{
                    display: inline-block;
                    margin-top: 20px;
                    color: #00f6ff;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <h1>❌ Erreur de fusion</h1>
                <p>Une erreur s'est produite lors de la fusion du dossier "<strong>{os.path.basename(folder_path)}</strong>".</p>
                <p><small>Erreur: {str(e)}</small></p>
                <p><a href="javascript:window.close()" class="back-link">← Fermer cette fenêtre</a></p>
            </div>
        </body>
        </html>
        """

@app.route('/fusionner', methods=['GET'])
def fusionner_dossier():
    """Fusionne tous les fichiers d'un dossier spécifique et retourne le HTML"""
    try:
        dossier = request.args.get('dossier', '').strip()

        if not dossier:
            return "Paramètre 'dossier' manquant", 400

        # Load category mapping
        mapping = {}
        if os.path.exists('category_mapping.json'):
            with open('category_mapping.json', 'r', encoding='utf-8') as f:
                mapping = json.load(f)
        
        # Get the actual folder path using resolver
        full_path = get_category_path(dossier)
        
        # Vérifier que le dossier existe
        if not os.path.exists(full_path):
            return f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Erreur - Dossier introuvable</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #1a1a1a;
                        color: #e0e0e0;
                        padding: 20px;
                        text-align: center;
                    }}
                    .error-container {{
                        max-width: 600px;
                        margin: 50px auto;
                        background-color: #2b2b2b;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                    }}
                    h1 {{ color: #ff6b6b; }}
                    .back-link {{
                        display: inline-block;
                        margin-top: 20px;
                        color: #00f6ff;
                        text-decoration: none;
                    }}
                </style>
            </head>
            <body>
                <div class="error-container">
                    <h1>❌ Dossier introuvable</h1>
                    <p>Le dossier "<strong>{dossier}</strong>" n'existe pas ou ne contient pas de fichiers.</p>
                    <p>Chemin recherché: <code>{full_path}</code></p>
                    <p><a href="javascript:window.close()" class="back-link">← Fermer cette fenêtre</a></p>
                </div>
            </body>
            </html>
            """, 404

        # Récupérer tous les fichiers du dossier
        files = [f for f in os.listdir(full_path)
                if f.startswith(f'{dossier}_') and f.endswith('.txt')]

        if not files:
            return f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Aucun fichier - {dossier}</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #1a1a1a;
                        color: #e0e0e0;
                        padding: 20px;
                        text-align: center;
                    }}
                    .empty-container {{
                        max-width: 600px;
                        margin: 50px auto;
                        background-color: #2b2b2b;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                    }}
                    h1 {{ color: #81c784; }}
                    .back-link {{
                        display: inline-block;
                        margin-top: 20px;
                        color: #00f6ff;
                        text-decoration: none;
                    }}
                </style>
            </head>
            <body>
                <div class="empty-container">
                    <h1>📁 Dossier vide</h1>
                    <p>Le dossier "<strong>{dossier}</strong>" ne contient pas de fichiers texte.</p>
                    <p><a href="javascript:window.close()" class="back-link">← Fermer cette fenêtre</a></p>
                </div>
            </body>
            </html>
            """, 200

        # Trier les fichiers par date (du plus récent au plus ancien)
        files.sort(reverse=True)

        # Fusionner tous les fichiers
        merged_content = []
        for filename in files:
            filepath = os.path.join(dossier, filename)
            try:
                # Try different encodings (UTF-8 first, then others)
                encodings_to_try = ['utf-8', 'utf-8-sig', 'cp1252', 'latin-1', 'iso-8859-1']
                content = None

                for encoding in encodings_to_try:
                    try:
                        with open(filepath, 'r', encoding=encoding) as f:
                            content = f.read()
                        # Replace problematic characters
                        content = content.replace('�', 'é')
                        content = content.replace('�', 'à')
                        content = content.replace('�', 'â')
                        content = content.replace('�', 'ê')
                        content = content.replace('�', 'î')
                        content = content.replace('�', 'ô')
                        content = content.replace('�', 'û')
                        content = content.replace('�', 'ç')
                        content = content.replace('�', 'ë')
                        content = content.replace('�', 'ï')
                        content = content.replace('�', 'ü')
                        break
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        print(f"Warning: Error reading {filepath} with {encoding}: {e}")
                        continue

                if content is None:
                    content = "❌ Erreur de lecture du fichier"

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

        # Fonction pour surligner tous les nombres en rouge
        def highlight_numbers(content):
            import re
            # Pattern simple pour tous les nombres (entiers, décimaux, formats de temps)
            number_pattern = r'\d{1,2}:\d{2}(?::\d{2})?|\b\d+(?:\.\d+)?\b'

            def replace_number(match):
                number_text = match.group(0)
                print(f"DEBUG: Replacing number: {number_text}")
                return '<span style="color: #ef4444; font-weight: bold;">' + number_text + '</span>'

            print(f"DEBUG: Content length before: {len(content)}")
            matches = re.findall(number_pattern, content)
            print(f"DEBUG: Found {len(matches)} numbers: {matches[:10]}")
            result = re.sub(number_pattern, replace_number, content)
            print(f"DEBUG: Content length after: {len(result)}")
            return result

        # Fonction pour surligner les dates (même logique que dans ton_projet)
        def highlight_dates(content):
            import re
            patterns = [
                r'\b\d{4}-\d{2}-\d{2}\b',  # ISO format: YYYY-MM-DD
                r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # US format: MM/DD/YYYY
                r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # European format: DD/MM/YYYY
                r'\b\d{1,2}-\d{1,2}-\d{4}\b',  # DD-MM-YYYY format
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Full month
                r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',  # DD Month YYYY
                r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b',  # Abbreviated month
                r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b'  # DD Month YYYY abbreviated
            ]
            date_pattern = '|'.join(patterns)

            def replace_date(match):
                date_text = match.group(0)
                return '<span style="color: #ff6b6b; font-weight: bold;">{}</span>'.format(date_text)

            return re.sub(date_pattern, replace_date, content, flags=re.IGNORECASE)

        # Surligner les dates et les nombres dans le contenu
        highlighted_content = highlight_dates(final_content)
        highlighted_content = highlight_numbers(highlighted_content)

        # Générer le HTML avec le style dark mode
        html_template = f"""
        <!DOCTYPE html>
        <html class=\"dark\" lang=\"fr\">
        <head>
            <meta charset=\"UTF-8\">
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
            <title>Fusion - {dossier}</title>
            <link href=\"https://fonts.googleapis.com\" rel=\"preconnect\"/>
            <link crossorigin=\"\" href=\"https://fonts.gstatic.com\" rel=\"preconnect\"/>
            <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&amp;display=swap\" rel=\"stylesheet\"/>
            <script src=\"https://cdn.tailwindcss.com?plugins=forms,container-queries\"></script>
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
        <body class=\"font-display bg-background-light dark:bg-background-dark text-stone-800 dark:text-stone-200\">
          <div class=\"flex flex-col min-h-screen\">
            <header class=\"sticky top-0 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-sm z-10\">
              <div class=\"container mx-auto px-4 sm:px-6 lg:px-8\">
                <div class=\"flex items-center justify-between h-16 border-b border-stone-200 dark:border-stone-800\">
                  <div class=\"flex items-center gap-4\">
                    <div class=\"text-primary size-7\">
                      <svg fill=\"none\" viewBox=\"0 0 48 48\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M42.4379 44C42.4379 44 36.0744 33.9038 41.1692 24C46.8624 12.9336 42.2078 4 42.2078 4L7.01134 4C7.01134 4 11.6577 12.932 5.96912 23.9969C0.876273 33.9029 7.27094 44 7.27094 44L42.4379 44Z\" fill=\"currentColor\"></path></svg>
                </div>
                    <h1 class=\"text-xl font-bold text-stone-900 dark:text-white\">Fusion - {dossier}</h1>
                </div>
                </div>
              </div>
            </header>

            <main class=\"flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-8\">
              <div class=\"max-w-4xl mx-auto space-y-6\">
                <div class=\"bg-white dark:bg-stone-800 rounded-lg shadow-md border border-stone-200 dark:border-stone-700 p-6\">
                  <div class=\"text-sm text-stone-600 dark:text-stone-400 mb-4\">📊 Dossier: <strong>{dossier}</strong> · Fichiers fusionnés: <strong>{len(files)}</strong> · Généré: <strong>{datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</strong></div>
                  <div class=\"prose prose-stone dark:prose-invert max-w-none\" style=\"white-space: pre-wrap;\">{highlighted_content}</div>
                </div>
                <div class=\"text-center\"><a href=\"javascript:window.close()\" class=\"inline-flex items-center bg-primary text-white rounded-md px-4 py-2 text-sm hover:bg-primary/90 transition-colors\">← Fermer cette fenêtre</a></div>
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
        return f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Erreur - Fusion {dossier}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                    padding: 20px;
                    text-align: center;
                }}
                .error-container {{
                    max-width: 600px;
                    margin: 50px auto;
                    background-color: #2b2b2b;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                }}
                h1 {{ color: #ff6b6b; }}
                .back-link {{
                    display: inline-block;
                    margin-top: 20px;
                    color: #00f6ff;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <h1>❌ Erreur de fusion</h1>
                <p>Une erreur s'est produite lors de la fusion du dossier "<strong>{dossier}</strong>".</p>
                <p><small>Erreur: {str(e)}</small></p>
                <p><a href="javascript:window.close()" class="back-link">← Fermer cette fenêtre</a></p>
            </div>
        </body>
        </html>
        """, 500

def fusion_files_from_folder_backend(folder_path):
    """Utilise exactement la même logique que journal_viewer.py"""
    try:
        # Import des modules nécessaires (même que journal_viewer.py)
        import tempfile
        import re
        from pathlib import Path

        # Créer l'objet JournalViewer pour utiliser ses méthodes
        class JournalViewer:
            def create_date_pattern(self):
                patterns = [
                    r'\b\d{4}-\d{2}-\d{2}\b',  # ISO format: YYYY-MM-DD
                    r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # US format: MM/DD/YYYY
                    r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # European format: DD/MM/YYYY
                    r'\b\d{1,2}-\d{1,2}-\d{4}\b',  # DD-MM-YYYY format
                    r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Full month
                    r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',  # DD Month YYYY
                    r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b',  # Abbreviated month
                    r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b'  # DD Month YYYY abbreviated
                ]
                return '|'.join(patterns)

            def read_and_merge_files(self, folder_path):
                """Read all text files from folder and merge their content (same as journal_viewer.py)"""
                merged_content = []
                folder_name = os.path.basename(folder_path)

                if not os.path.exists(folder_path):
                    raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")

                # Get all text files that start with folder name
                files = [f for f in os.listdir(folder_path)
                        if f.startswith(f'{folder_name}_') and f.endswith('.txt')]

                if not files:
                    return ""

                # Sort files by name (which contains dates)
                files.sort()

                # Read each file
                for filename in files:
                    filepath = os.path.join(folder_path, filename)
                    try:
                        # Try different encodings
                        encodings_to_try = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
                        content = None

                        for encoding in encodings_to_try:
                            try:
                                with open(filepath, 'r', encoding=encoding) as file:
                                    content = file.read()
                                break
                            except UnicodeDecodeError:
                                continue

                        if content is None:
                            content = "❌ Error reading file"

                        if content.strip():  # Only add non-empty files
                            # Add file header
                            merged_content.append(f"\n{'='*50}")
                            merged_content.append(f"FILE: {filename}")
                            merged_content.append(f"{'='*50}\n")
                            merged_content.append(content)
                            merged_content.append("\n")

                    except Exception as e:
                        print(f"Warning: Could not read file {filepath}: {e}")
                        continue

                return '\n'.join(merged_content)

            def highlight_dates(self, content):
                """Highlight all dates in the content using regex replacement (same as journal_viewer.py)"""
                date_pattern = self.create_date_pattern()

                def replace_date(match):
                    date_text = match.group(0)
                    return f'<span style="color: #ff6b6b; font-weight: bold;">{date_text}</span>'

                # Apply highlighting
                highlighted_content = re.sub(date_pattern, replace_date, content, flags=re.IGNORECASE)
                return highlighted_content

            def highlight_numbers(self, content):
                """Highlight all numbers in the content using regex replacement"""
                number_pattern = r'\d{1,2}:\d{2}(?::\d{2})?|\b\d+(?:\.\d+)?\b'

                def replace_number(match):
                    number_text = match.group(0)
                    return f'<span style="color: #ef4444; font-weight: bold;">{number_text}</span>'

                # Apply highlighting
                highlighted_content = re.sub(number_pattern, replace_number, content)
                return highlighted_content

            def generate_html(self, content, title="Journal Viewer - Dark Mode"):
                """Generate HTML with dark mode styling (same as journal_viewer.py)"""
                html_template = """
        <!DOCTYPE html>
                <html class=\"dark\" lang=\"en\">
        <head>
                    <meta charset=\"UTF-8\">
                    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
            <title>{title}</title>
                    <link href=\"https://fonts.googleapis.com\" rel=\"preconnect\"/>
                    <link crossorigin=\"\" href=\"https://fonts.gstatic.com\" rel=\"preconnect\"/>
                    <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&amp;display=swap\" rel=\"stylesheet\"/>
                    <script src=\"https://cdn.tailwindcss.com?plugins=forms,container-queries\"></script>
                    <script>
                      tailwind.config = {
                        darkMode: "class",
                        theme: {
                          extend: {
                            colors: {
                              "primary": "#137fec",
                              "background-light": "#f6f7f8",
                              "background-dark": "#101922",
                              "red-number": "#ef4444",
                            },
                            fontFamily: {
                              "display": ["Inter"]
                            },
                            borderRadius: {
                              "DEFAULT": "0.25rem",
                              "lg": "0.5rem",
                              "xl": "0.75rem",
                              "full": "9999px"
                            },
                          },
                        },
                      }
                    </script>
                    <style>
                      /* Numbers are already styled inline with color and font-weight */
                    </style>
        </head>
                    <body class=\"font-display bg-background-light dark:bg-background-dark text-stone-800 dark:text-stone-200\">
                      <div class=\"flex flex-col min-h-screen\">
                        <header class=\"sticky top-0 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-sm z-10\">
                          <div class=\"container mx-auto px-4 sm:px-6 lg:px-8\">
                            <div class=\"flex items-center justify-between h-16 border-b border-stone-200 dark:border-stone-800\">
                              <div class=\"flex items-center gap-4\">
                                <div class=\"text-primary size-7\">
                                  <svg fill=\"none\" viewBox=\"0 0 48 48\" xmlns=\"http://www.w3.org/2000/svg\">
                                    <path d=\"M42.4379 44C42.4379 44 36.0744 33.9038 41.1692 24C46.8624 12.9336 42.2078 4 42.2078 4L7.01134 4C7.01134 4 11.6577 12.932 5.96912 23.9969C0.876273 33.9029 7.27094 44 7.27094 44L42.4379 44Z\" fill=\"currentColor\"></path>
                                  </svg>
                </div>
                                <h1 class=\"text-xl font-bold text-stone-900 dark:text-white\">{title}</h1>
                              </div>
                            </div>
                          </div>
                        </header>

                        <main class=\"flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-8\">
                          <div class=\"max-w-4xl mx-auto\">
                            <div class=\"bg-white dark:bg-stone-800 rounded-lg shadow-md border border-stone-200 dark:border-stone-700 p-6\">
                              <div class=\"prose prose-stone dark:prose-invert max-w-none\" style=\"white-space: pre-wrap;\">{content}</div>
                            </div>
                          </div>
                        </main>
            </div>
        </body>
        </html>
        """

                return html_template.replace("{content}", content).replace("{title}", title)

        # Utiliser la classe JournalViewer pour traiter les fichiers
        viewer = JournalViewer()

        # Read and merge all text files
        merged_content = viewer.read_and_merge_files(folder_path)

        if not merged_content.strip():
            return f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Aucun fichier trouvé</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #1a1a1a;
                        color: #e0e0e0;
                        padding: 20px;
                        text-align: center;
                    }}
                    .empty-container {{
                        max-width: 600px;
                        margin: 50px auto;
                        background-color: #2b2b2b;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                    }}
                    h1 {{ color: #81c784; }}
                    .back-link {{
                        display: inline-block;
                        margin-top: 20px;
                        color: #00f6ff;
                        text-decoration: none;
                    }}
                </style>
            </head>
            <body>
                <div class="empty-container">
                    <h1>📁 Dossier vide</h1>
                    <p>Le dossier "<strong>{os.path.basename(folder_path)}</strong>" ne contient pas de fichiers texte.</p>
                    <p><a href="javascript:window.close()" class="back-link">← Fermer cette fenêtre</a></p>
                </div>
            </body>
            </html>
            """

        # Highlight dates and numbers
        highlighted_content = viewer.highlight_dates(merged_content)
        highlighted_content = viewer.highlight_numbers(highlighted_content)

        # Generate HTML with correct title (fix encoding)
        title = os.path.basename(folder_path)
        # Fix encoding in title
        title = title.replace('├', '').replace('⌐', 'é').replace('├', '').replace('â', "'").replace('€', '€')
        html_content = viewer.generate_html(highlighted_content, f"Fusion - {title}")

        return html_content

    except Exception as e:
        print(f"Erreur lors de la fusion du dossier {folder_path}: {str(e)}")
        return f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Erreur de fusion</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                    padding: 20px;
                    text-align: center;
                }}
                .error-container {{
                    max-width: 600px;
                    margin: 50px auto;
                    background-color: #2b2b2b;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                }}
                h1 {{ color: #ff6b6b; }}
                .back-link {{
                    display: inline-block;
                    margin-top: 20px;
                    color: #00f6ff;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <h1>❌ Erreur de fusion</h1>
                <p>Une erreur s'est produite lors de la fusion du dossier "<strong>{os.path.basename(folder_path)}</strong>".</p>
                <p><small>Erreur: {str(e)}</small></p>
                <p><a href="javascript:window.close()" class="back-link">← Fermer cette fenêtre</a></p>
            </div>
        </body>
        </html>
        """

@app.route('/fusionner_backend', methods=['GET'])
def fusionner_dossier_backend():
    """Route qui utilise exactement la même logique que journal_viewer.py"""
    try:
        dossier = request.args.get('dossier', '').strip()

        if not dossier:
            html_error = """
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Erreur - Paramètre manquant</title>
            </head>
            <body>
                <h1>❌ Paramètre 'dossier' manquant</h1>
            </body>
            </html>
            """
            resp = make_response(html_error)
            resp.headers['Content-Type'] = 'text/html; charset=utf-8'
            resp.status_code = 400
            return resp

        # Load category mapping
        mapping = {}
        if os.path.exists('category_mapping.json'):
            with open('category_mapping.json', 'r', encoding='utf-8') as f:
                mapping = json.load(f)
        
        # Get the actual folder path using resolver
        folder_path = get_absolute_category_path(dossier)

        # Utiliser exactement la même logique que journal_viewer.py
        html_content = fusion_files_from_folder_backend(folder_path)

        # S'assurer que le navigateur affiche le HTML rendu, pas le HTML brut
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response

    except Exception as e:
        print(f"Erreur lors de la fusion du dossier {dossier}: {str(e)}")
        html_error = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Erreur - Fusion {dossier}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                    padding: 20px;
                    text-align: center;
                }}
                .error-container {{
                    max-width: 600px;
                    margin: 50px auto;
                    background-color: #2b2b2b;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                }}
                h1 {{ color: #ff6b6b; }}
                .back-link {{
                    display: inline-block;
                    margin-top: 20px;
                    color: #00f6ff;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <h1>❌ Erreur de fusion</h1>
                <p>Une erreur s'est produite lors de la fusion du dossier "<strong>{dossier}</strong>".</p>
                <p><small>Erreur: {str(e)}</small></p>
                <p><a href="javascript:window.close()" class="back-link">← Fermer cette fenêtre</a></p>
            </div>
        </body>
        </html>
        """
        resp = make_response(html_error)
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        resp.status_code = 500
        return resp

# Import hierarchical categories handler
from routes_structured import get_categories_structured_handler

@app.route('/categories_structured')
def get_categories_structured():
    """Endpoint for hierarchical folder structure"""
    return get_categories_structured_handler(load_categories)

if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5008))
    print("Demarrage du serveur Flask...")
    print("Serveur accessible sur: http://localhost:{}".format(port))
    print("Page de notes: http://localhost:{}/all_notes".format(port))
    print("Assurez-vous que le serveur de recherche Node.js est demarre (port 3008)")
    try:
        app.run(debug=debug_mode, host='0.0.0.0', port=port)
    except UnicodeEncodeError:
        # Fallback without emojis if encoding fails
        print("Starting Flask server (fallback mode)...")
        print("Server available at: http://localhost:{}".format(port))
        print("Notes page: http://localhost:{}/all_notes".format(port))
        print("Make sure Node.js search server is running (port 3008)")
        app.run(debug=debug_mode, host='0.0.0.0', port=port)