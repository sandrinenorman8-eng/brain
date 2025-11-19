"""
Routes pour les endpoints de fusion avec support du mapping hiérarchique
"""
from flask import request, make_response
import os
from category_path_resolver import get_absolute_category_path

def register_fusion_routes(app):
    """Enregistre les routes de fusion dans l'application Flask"""
    
    @app.route('/fusionner_fixed', methods=['GET'])
    def fusionner_dossier_fixed():
        """Fusion avec support du mapping hiérarchique"""
        try:
            dossier = request.args.get('dossier', '').strip()
            
            if not dossier:
                return "Paramètre 'dossier' manquant", 400
            
            # Utiliser le resolver pour obtenir le bon chemin
            full_path = get_absolute_category_path(dossier)
            
            # Vérifier que le dossier existe
            if not os.path.exists(full_path):
                html_error = f"""
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
                        <p>Le dossier "<strong>{dossier}</strong>" n'existe pas.</p>
                        <p>Chemin recherché: <code>{full_path}</code></p>
                        <p><a href="javascript:window.close()" class="back-link">← Fermer cette fenêtre</a></p>
                    </div>
                </body>
                </html>
                """
                resp = make_response(html_error)
                resp.headers['Content-Type'] = 'text/html; charset=utf-8'
                resp.status_code = 404
                return resp
            
            # Récupérer tous les fichiers du dossier
            folder_name = os.path.basename(full_path)
            files = [f for f in os.listdir(full_path)
                    if f.startswith(f'{folder_name}_') and f.endswith('.txt')]
            
            if not files:
                html_error = f"""
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Aucun fichier - {dossier}</title>
                </head>
                <body>
                    <h1>📂 Aucun fichier trouvé</h1>
                    <p>Le dossier "{dossier}" ne contient aucun fichier.</p>
                </body>
                </html>
                """
                return html_error, 404
            
            # Fusionner les fichiers
            files.sort()
            merged_content = []
            
            for filename in files:
                filepath = os.path.join(full_path, filename)
                try:
                    encodings_to_try = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
                    content = None
                    
                    for encoding in encodings_to_try:
                        try:
                            with open(filepath, 'r', encoding=encoding) as f:
                                content = f.read()
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if content:
                        merged_content.append(f"=== {filename} ===\n{content}\n")
                except Exception as e:
                    merged_content.append(f"=== Erreur lecture {filename}: {e} ===\n")
            
            # Générer le HTML
            html_content = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Fusion - {dossier}</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #1a1a1a;
                        color: #e0e0e0;
                        padding: 20px;
                        max-width: 1200px;
                        margin: 0 auto;
                    }}
                    h1 {{
                        color: #00f6ff;
                        border-bottom: 2px solid #00f6ff;
                        padding-bottom: 10px;
                    }}
                    pre {{
                        background-color: #2b2b2b;
                        padding: 20px;
                        border-radius: 8px;
                        white-space: pre-wrap;
                        line-height: 1.6;
                    }}
                </style>
            </head>
            <body>
                <h1>🔗 Fusion: {dossier}</h1>
                <p>Nombre de fichiers: {len(files)}</p>
                <pre>{''.join(merged_content)}</pre>
            </body>
            </html>
            """
            
            resp = make_response(html_content)
            resp.headers['Content-Type'] = 'text/html; charset=utf-8'
            return resp
            
        except Exception as e:
            html_error = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Erreur de fusion</title>
            </head>
            <body>
                <h1>❌ Erreur de fusion</h1>
                <p>Erreur: {str(e)}</p>
            </body>
            </html>
            """
            resp = make_response(html_error)
            resp.headers['Content-Type'] = 'text/html; charset=utf-8'
            resp.status_code = 500
            return resp
