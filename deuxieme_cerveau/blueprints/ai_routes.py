# -*- coding: utf-8 -*-
"""
Routes pour l'organisation intelligente des fusions
"""

from flask import Blueprint, request, jsonify
import os
import sys

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.ai_service import AIService
from utils.file_utils import safe_read, safe_write
from utils.response_utils import success_response, error_response
import datetime

ai_bp = Blueprint('ai', __name__)
ai_service = AIService()

@ai_bp.route('/organize', methods=['POST'])
def organize_fusion():
    """Organise une fusion de catégorie avec l'IA"""
    try:
        data = request.get_json()
        fusion_file = data.get('fusion_file')
        category_name = data.get('category_name', 'Notes')
        
        if not fusion_file:
            return error_response("Fichier de fusion requis", 400)
        
        # Lire le contenu de la fusion
        fusion_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), fusion_file)
        
        if not os.path.exists(fusion_path):
            return error_response(f"Fichier non trouvé: {fusion_file}", 404)
        
        fusion_content = safe_read(fusion_path)
        
        # Organiser avec l'IA
        result = ai_service.organize_fusion(fusion_content, category_name)
        
        if not result['success']:
            return error_response(result.get('error', 'Erreur IA'), 500)
        
        # Sauvegarder le résultat organisé
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        organized_filename = f"organized_{category_name}_{timestamp}.md"
        organized_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fusion_organized')
        
        os.makedirs(organized_folder, exist_ok=True)
        organized_path = os.path.join(organized_folder, organized_filename)
        
        safe_write(organized_path, result['organized_content'], create_backup=False)
        
        return success_response({
            "organized_content": result['organized_content'],
            "filename": organized_filename,
            "path": f"fusion_organized/{organized_filename}",
            "category": category_name
        }, "Fusion organisée avec succès")
        
    except Exception as e:
        return error_response(str(e), 500)

@ai_bp.route('/test', methods=['GET'])
def test_ai():
    """Teste la connexion à l'API IA"""
    try:
        is_connected = ai_service.test_connection()
        
        if is_connected:
            return success_response({"status": "connected"}, "API IA connectée")
        else:
            return error_response("API IA non disponible", 503)
            
    except Exception as e:
        return error_response(str(e), 500)

@ai_bp.route('/list_fusions', methods=['GET'])
def list_fusions():
    """Liste SEULEMENT les dernières fusions (1 globale + 1 par catégorie)"""
    try:
        fusions = []
        
        # 1 SEULE fusion globale (la plus récente)
        global_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fusion_global')
        if os.path.exists(global_folder):
            global_files = [f for f in os.listdir(global_folder) if f.endswith('.txt') and 'globale' in f]
            if global_files:
                # Trier par date (nom de fichier) et prendre le plus récent
                latest_global = sorted(global_files, reverse=True)[0]
                fusions.append({
                    "filename": latest_global,
                    "path": f"fusion_global/{latest_global}",
                    "type": "global",
                    "display_name": "🌍 Fusion Globale (toutes catégories)"
                })
        
        # 1 fusion par catégorie (la plus récente de chaque)
        cat_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fusion_categories')
        if os.path.exists(cat_folder):
            # Grouper par catégorie
            categories = {}
            for file in os.listdir(cat_folder):
                if file.endswith('.txt'):
                    # Extraire le nom de catégorie
                    cat_name = file.replace('fusion_categories_', '').replace('fusion_', '')
                    cat_name = cat_name.rsplit('_', 3)[0]  # Enlever la date
                    
                    if cat_name not in categories:
                        categories[cat_name] = []
                    categories[cat_name].append(file)
            
            # Prendre le plus récent de chaque catégorie
            for cat_name, files in categories.items():
                latest_file = sorted(files, reverse=True)[0]
                fusions.append({
                    "filename": latest_file,
                    "path": f"fusion_categories/{latest_file}",
                    "type": "category",
                    "display_name": f"📁 {cat_name.replace('_', ' ').title()}"
                })
        
        # Trier : globale en premier, puis catégories par ordre alphabétique
        fusions.sort(key=lambda x: (x['type'] != 'global', x.get('display_name', '')))
        
        return success_response({"fusions": fusions}, f"{len(fusions)} fusions disponibles")
        
    except Exception as e:
        return error_response(str(e), 500)
