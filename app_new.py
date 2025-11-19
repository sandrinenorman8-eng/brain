from flask import Flask, jsonify
from config.config import Config
from blueprints.category_routes import category_bp
from blueprints.notes_routes import notes_bp
from blueprints.search_routes import search_bp
from blueprints.web_routes import web_bp
from blueprints.utility_routes import utility_bp
from blueprints.fusion_routes import fusion_bp

# Import IA blueprint (optionnel - ne casse rien si absent)
try:
    from blueprints.ai_routes import ai_bp
    AI_AVAILABLE = True
except Exception as e:
    print(f"IA non chargée: {e}")
    AI_AVAILABLE = False

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    # CORS simple sans dépendance
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        return response
    
    app.register_blueprint(category_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(web_bp)
    app.register_blueprint(utility_bp)
    app.register_blueprint(fusion_bp)
    
    # Enregistrer blueprint IA si disponible
    if AI_AVAILABLE:
        app.register_blueprint(ai_bp, url_prefix='/ai')
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Resource not found",
            "error_type": "NotFound"
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "error_type": "InternalServerError"
        }), 500
    
    return app

app = create_app()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5008))
    app.run(host='0.0.0.0', port=port, debug=False)
    
    try:
        print("Démarrage du serveur Flask...")
        print(f"Serveur accessible sur: http://localhost:{Config.PORT}")
        print(f"Page de notes: http://localhost:{Config.PORT}/all_notes")
        print("Assurez-vous que le serveur de recherche Node.js est démarré (port 3008)")
        
        app.run(
            debug=Config.FLASK_DEBUG,
            host=Config.HOST,
            port=Config.PORT
        )
    except UnicodeEncodeError:
        print("Starting Flask server (fallback mode)...")
        print(f"Server available at: http://localhost:{Config.PORT}")
        print(f"Notes page: http://localhost:{Config.PORT}/all_notes")
        print("Make sure Node.js search server is running (port 3008)")
        
        app.run(
            debug=Config.FLASK_DEBUG,
            host=Config.HOST,
            port=Config.PORT
        )
