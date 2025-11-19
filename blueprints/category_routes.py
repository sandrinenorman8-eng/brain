from flask import Blueprint, request, jsonify
from services.category_service import load_categories, add_category, delete_category
from services.notes_service import _get_all_files_cached

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    """Retourne la liste des catégories (format ancien pour compatibilité)"""
    return jsonify(load_categories())

@category_bp.route('/add_category', methods=['POST'])
def create_category():
    """Crée une nouvelle catégorie (format ancien pour compatibilité)"""
    try:
        data = request.json
        name = data.get('name', '').strip().lower()
        
        if not name:
            return jsonify({"error": "Category name is required"}), 400
        
        new_category = add_category(name)
        _get_all_files_cached.cache_clear()
        
        return jsonify(new_category)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@category_bp.route('/erase_category/<category>', methods=['DELETE'])
def remove_category(category):
    """Supprime une catégorie (format ancien pour compatibilité)"""
    try:
        delete_category(category)
        _get_all_files_cached.cache_clear()
        
        return jsonify({
            "status": "deleted",
            "category": category,
            "message": f"Category '{category}' and all its files have been deleted"
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@category_bp.route('/open_folder/<category>', methods=['GET'])
def open_folder(category):
    """Ouvre le dossier de la catégorie dans l'Explorateur Windows"""
    import subprocess
    import platform
    import os
    from flask import jsonify
    from category_path_resolver import get_absolute_category_path
    from services.category_service import load_categories

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
