from flask import Blueprint, request
import os
import platform
import subprocess
import zipfile
from datetime import datetime
from utils.response_utils import success_response, error_response
from services.fusion_service import fusion_global, fusion_by_category, fusion_single_category
from services.category_service import load_categories
from category_path_resolver import get_absolute_category_path

utility_bp = Blueprint('utility', __name__, url_prefix='/api')

@utility_bp.route('/fusion/global', methods=['POST'])
def fusion_global_route():
    try:
        result = fusion_global()
        return success_response(result, "Global fusion successful")
    except Exception as e:
        return error_response(str(e), 500, "InternalServerError")

@utility_bp.route('/fusion/category', methods=['POST'])
def fusion_category_route():
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return error_response("Invalid JSON data", 400)
        
        selected_categories = data.get('categories', [])
        
        if not selected_categories:
            return error_response("No categories selected", 400)
        
        result = fusion_by_category(selected_categories)
        return success_response(result, "Category fusion successful")
    
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500, "InternalServerError")

@utility_bp.route('/fusion/single-category', methods=['POST'])
def fusion_single_category_route():
    try:
        data = request.get_json()
        category_name = data.get('category')
        
        if not category_name:
            return error_response("Category name is required", 400)
        
        result = fusion_single_category(category_name)
        return success_response(result, f"Fusion of category '{category_name}' successful")
    
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500, "InternalServerError")

@utility_bp.route('/open_folder/<category>', methods=['GET'])
def open_folder_route(category):
    if platform.system() != 'Windows':
        return error_response("This feature is only available on Windows", 400)
    
    try:
        categories = load_categories()
        if not any(c['name'] == category for c in categories):
            return error_response("Category not found", 404, "NotFound")
        
        folder_path = get_absolute_category_path(category)
        os.makedirs(folder_path, exist_ok=True)
        
        folder_path_normalized = os.path.normpath(folder_path)
        
        try:
            os.startfile(folder_path_normalized)
        except Exception:
            subprocess.Popen(f'explorer "{folder_path_normalized}"', shell=True)
        
        return success_response({
            "path": folder_path_normalized
        }, "Folder opened successfully")
    
    except Exception as e:
        return error_response(str(e), 500, "InternalServerError")

@utility_bp.route('/backup_project', methods=['POST'])
def backup_project_route():
    try:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        memobrik_dir = os.path.dirname(os.getcwd())
        
        backup_filename = f"backup_memobrik_complet_{date_str}.zip"
        
        zip_dir = os.path.join(memobrik_dir, 'zip')
        os.makedirs(zip_dir, exist_ok=True)
        
        backup_path = os.path.join(zip_dir, backup_filename)
        
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(memobrik_dir):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and d != 'node_modules' and d != 'zip']
                
                for file in files:
                    if not file.startswith('.') and not file.endswith('.pyc'):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, memobrik_dir)
                        zipf.write(file_path, arcname)
        
        if os.path.exists(backup_path):
            file_size = os.path.getsize(backup_path)
            file_size_mb = round(file_size / (1024 * 1024), 2)
            
            return success_response({
                "filename": backup_filename,
                "path": backup_path,
                "size_mb": file_size_mb,
                "date": date_str,
                "scope": "Complete memobrik folder"
            }, "Complete backup created successfully")
        else:
            return error_response("Error creating backup file", 500, "InternalServerError")
    
    except Exception as e:
        return error_response(str(e), 500, "InternalServerError")



@utility_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for search functionality"""
    return success_response({
        "status": "running",
        "message": "Search service active (integrated in Flask)"
    }, "Service is healthy")
