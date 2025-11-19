from flask import Blueprint, request, jsonify, make_response
import os
import re
from datetime import datetime
from category_path_resolver import get_category_path, get_absolute_category_path
from services.fusion_service import fusion_global, fusion_by_category, fusion_single_category
from services.category_service import load_categories
from utils.file_utils import safe_read

fusion_bp = Blueprint('fusion', __name__, url_prefix='/api')

@fusion_bp.route('/fusion/global', methods=['POST'])
def fusion_global_route():
    """Fusionne toutes les notes de toutes les catégories en un seul fichier"""
    try:
        result = fusion_global()
        return jsonify({
            "success": True,
            "message": f"Fusion globale réussie ! Fichier créé: {result['filename']}",
            **result
        })
    except Exception as e:
        print(f"Erreur lors de la fusion globale: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@fusion_bp.route('/fusion/category', methods=['POST'])
def fusion_category_route():
    """Fusionne les notes des catégories sélectionnées"""
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"success": False, "error": "Données JSON invalides"}), 400
        
        selected_categories = data.get('categories', [])
        
        if not selected_categories:
            return jsonify({"success": False, "error": "Aucune catégorie sélectionnée"}), 400
        
        result = fusion_by_category(selected_categories)
        return jsonify({
            "success": True,
            "message": f"Fusion par catégories réussie ! Fichier créé: {result['filename']}",
            **result
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        print(f"Erreur lors de la fusion par catégories: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@fusion_bp.route('/fusion/single-category', methods=['POST'])
def fusion_single_category_route():
    """Fusionne tous les fichiers d'une seule catégorie"""
    try:
        data = request.get_json()
        category_name = data.get('category')
        
        if not category_name:
            return jsonify({"success": False, "error": "Nom de catégorie manquant"}), 400
        
        result = fusion_single_category(category_name)
        return jsonify({
            "success": True,
            "message": f"Fusion de la catégorie '{category_name}' réussie ! Fichier créé: {result['filename']}",
            **result
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        print(f"Erreur lors de la fusion de la catégorie: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

def create_date_pattern():
    """Create a comprehensive regex pattern for date detection"""
    patterns = [
        r'\b\d{4}-\d{2}-\d{2}\b',
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',
        r'\b\d{1,2}-\d{1,2}-\d{4}\b',
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b'
    ]
    return '|'.join(patterns)

def highlight_dates(content):
    """Highlight all dates in the content"""
    date_pattern = create_date_pattern()
    
    def replace_date(match):
        date_text = match.group(0)
        return f'<span style="color: #ff6b6b; font-weight: bold;">{date_text}</span>'
    
    return re.sub(date_pattern, replace_date, content, flags=re.IGNORECASE)

def highlight_numbers(content):
    """Highlight all numbers in the content"""
    number_pattern = r'\d{1,2}:\d{2}(?::\d{2})?|\b\d+(?:\.\d+)?\b'
    
    def replace_number(match):
        number_text = match.group(0)
        return f'<span style="color: #ef4444; font-weight: bold;">{number_text}</span>'
    
    return re.sub(number_pattern, replace_number, content)

def generate_fusion_html(content, title, dossier, file_count):
    """Generate HTML for fusion view"""
    html_template = f"""
<!DOCTYPE html>
<html class="dark" lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
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
            <h1 class="text-xl font-bold text-stone-900 dark:text-white">{title}</h1>
          </div>
        </div>
      </div>
    </header>

    <main class="flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="max-w-4xl mx-auto space-y-6">
        <div class="bg-white dark:bg-stone-800 rounded-lg shadow-md border border-stone-200 dark:border-stone-700 p-6">
          <div class="text-sm text-stone-600 dark:text-stone-400 mb-4">📊 Dossier: <strong>{dossier}</strong> · Fichiers fusionnés: <strong>{file_count}</strong> · Généré: <strong>{datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</strong></div>
          <div class="prose prose-stone dark:prose-invert max-w-none" style="white-space: pre-wrap;">{content}</div>
        </div>
        <div class="text-center"><a href="javascript:window.close()" class="inline-flex items-center bg-primary text-white rounded-md px-4 py-2 text-sm hover:bg-primary/90 transition-colors">← Fermer cette fenêtre</a></div>
      </div>
    </main>
  </div>
</body>
</html>
"""
    return html_template

@fusion_bp.route('/fusionner', methods=['GET'])
def fusionner_dossier():
    """Fusionne tous les fichiers d'un dossier spécifique et retourne le HTML"""
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
        
        # Surligner les dates et les nombres
        highlighted_content = highlight_dates(final_content)
        highlighted_content = highlight_numbers(highlighted_content)
        
        # Générer le HTML
        html_content = generate_fusion_html(
            highlighted_content,
            f"Fusion - {dossier}",
            dossier,
            len(files)
        )
        
        resp = make_response(html_content)
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'
        return resp
        
    except Exception as e:
        print(f"Erreur lors de la fusion du dossier {dossier}: {str(e)}")
        return f"Erreur: {str(e)}", 500

