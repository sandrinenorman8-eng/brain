from flask import Blueprint, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from utils.response_utils import success_response, error_response
from services.notes_service import save_note, list_notes, read_note, get_all_files, _get_all_files_cached
from services.category_service import load_categories, get_category_info
from category_path_resolver import get_category_path

notes_bp = Blueprint('notes', __name__)

# Routes avec préfixe /api/ pour la nouvelle API
# Routes sans préfixe pour compatibilité avec l'ancien frontend

@notes_bp.route('/save/<category>', methods=['POST'])
def save_note_route(category):
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return error_response("Note text is required", 400)
        
        filename = save_note(category, text)
        
        return success_response(
            {"filename": filename},
            "Note saved successfully"
        )
    
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500, "InternalServerError")

@notes_bp.route('/list/<category>', methods=['GET'])
def list_notes_route(category):
    try:
        files = list_notes(category)
        return success_response(files)
    except Exception as e:
        return error_response(str(e), 500, "InternalServerError")

@notes_bp.route('/read/<category>/<filename>', methods=['GET'])
def read_note_route(category, filename):
    try:
        import urllib.parse
        category = urllib.parse.unquote(category)
        filename = urllib.parse.unquote(filename)
        
        content = read_note(category, filename)
        
        date_formatted = filename.replace(f'{category}_', '').replace('.txt', '').split('-')
        date_formatted = f"{date_formatted[2]}/{date_formatted[1]}/{date_formatted[0]}"
        
        cat_info = get_category_info(category) or {'emoji': '📁', 'color': '#666'}
        
        html = f"""
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
        
        return html
    
    except FileNotFoundError:
        return "File not found", 404
    except Exception as e:
        return error_response(str(e), 500, "InternalServerError")

@notes_bp.route('/all_files', methods=['GET'])
def all_files_route():
    try:
        files = get_all_files()
        return success_response(files)
    except Exception as e:
        return error_response(str(e), 500, "InternalServerError")

@notes_bp.route('/upload_file', methods=['POST'])
def upload_file_route():
    try:
        if 'file' not in request.files:
            return error_response("No file provided", 400)
        
        file = request.files['file']
        category = request.form.get('category', '').strip()
        
        if file.filename == '':
            return error_response("Empty filename", 400)
        
        if not category:
            return error_response("Category not specified", 400)
        
        categories = load_categories()
        if not any(c['name'] == category for c in categories):
            return error_response("Invalid category", 400)
        
        filename = secure_filename(file.filename)
        if not filename:
            return error_response("Invalid filename", 400)
        
        category_path = get_category_path(category)
        os.makedirs(category_path, exist_ok=True)
        
        filepath = os.path.join(category_path, filename)
        if os.path.exists(filepath):
            name, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(filepath):
                filename = f"{name}_{counter}{ext}"
                filepath = os.path.join(category_path, filename)
                counter += 1
        
        file.save(filepath)
        
        file_size = os.path.getsize(filepath)
        file_size_kb = round(file_size / 1024, 2)
        
        _get_all_files_cached.cache_clear()
        
        return success_response({
            "filename": filename,
            "category": category,
            "path": filepath,
            "size_kb": file_size_kb
        }, "File uploaded successfully")
    
    except Exception as e:
        return error_response(str(e), 500, "InternalServerError")

# Routes avec préfixe /api/ pour nouvelle API
@notes_bp.route('/api/save/<category>', methods=['POST'])
def save_note_route_api(category):
    return save_note_route(category)

@notes_bp.route('/api/list/<category>', methods=['GET'])
def list_notes_route_api(category):
    return list_notes_route(category)

@notes_bp.route('/api/read/<category>/<filename>', methods=['GET'])
def read_note_route_api(category, filename):
    return read_note_route(category, filename)

@notes_bp.route('/api/all_files', methods=['GET'])
def all_files_route_api():
    return all_files_route()

@notes_bp.route('/api/upload_file', methods=['POST'])
def upload_file_route_api():
    return upload_file_route()

# Routes de compatibilité format ancien (sans success/data wrapper)
from flask import jsonify

@notes_bp.route('/all_files_compat', methods=['GET'])
def all_files_compat():
    files = get_all_files()
    return jsonify(files)

@notes_bp.route('/api/knowledge-graph', methods=['GET'])
def knowledge_graph_data():
    try:
        all_files = get_all_files()
        notes_data = []
        for file_info in all_files:
            content = read_note(file_info['category'], file_info['filename'])
            tags = [line.strip().replace('#', '') for line in content.split('\n') if line.strip().startswith('#')]
            notes_data.append({
                'id': file_info['filename'],
                'summary': content[:100],
                'tags': tags
            })
        return success_response(notes_data)
    except Exception as e:
        return error_response(str(e), 500, "InternalServerError")
