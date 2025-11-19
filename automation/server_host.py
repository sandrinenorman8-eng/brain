#!/usr/bin/env python3
"""
Memobrik Server Auto-Starter - Native Messaging Host
Volet 1 : Native Messaging (Solution Principale)
"""

import sys
import subprocess
import json
import time
import requests
import os
import logging
from pathlib import Path

# Configuration
SERVER_PORT = 5008
SERVER_PATH = r"G:\memobrik\deuxieme_cerveau"
START_SCRIPT = "START.bat"
HEALTH_ENDPOINT = f"http://localhost:{SERVER_PORT}/health"
MAX_STARTUP_TIME = 20  # secondes

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(__file__).parent / 'server_host.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def is_server_running():
    """Vérifie si le serveur Flask est déjà en cours d'exécution"""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_server():
    """Démarre le serveur Flask si nécessaire"""
    logger.info("Vérification de l'état du serveur...")
    
    if is_server_running():
        logger.info("Serveur déjà en cours d'exécution")
        return {"status": "already_running", "port": SERVER_PORT}
    
    try:
        logger.info(f"Démarrage du serveur depuis {SERVER_PATH}")
        
        # Vérifier que le chemin existe
        if not os.path.exists(SERVER_PATH):
            logger.error(f"Chemin non trouvé: {SERVER_PATH}")
            return {"status": "error", "message": f"Chemin non trouvé: {SERVER_PATH}"}
        
        # Vérifier que le script de démarrage existe
        start_script_path = os.path.join(SERVER_PATH, START_SCRIPT)
        if not os.path.exists(start_script_path):
            logger.error(f"Script de démarrage non trouvé: {start_script_path}")
            return {"status": "error", "message": f"Script non trouvé: {START_SCRIPT}"}
        
        # Démarrer le serveur en arrière-plan
        subprocess.Popen(
            [start_script_path], 
            shell=True, 
            cwd=SERVER_PATH,
            creationflags=subprocess.CREATE_NO_WINDOW  # Masquer la fenêtre
        )
        
        logger.info("Attente du démarrage du serveur...")
        
        # Attendre que le serveur soit prêt
        for attempt in range(MAX_STARTUP_TIME):
            time.sleep(1)
            if is_server_running():
                logger.info(f"Serveur démarré avec succès (tentative {attempt + 1})")
                return {"status": "started", "port": SERVER_PORT}
        
        logger.warning("Timeout lors du démarrage du serveur")
        return {"status": "timeout", "message": f"Serveur non prêt après {MAX_STARTUP_TIME}s"}
        
    except Exception as e:
        logger.error(f"Erreur lors du démarrage: {str(e)}")
        return {"status": "error", "message": str(e)}

def add_health_endpoint():
    """Ajoute un endpoint de santé au serveur Flask si nécessaire"""
    health_code = '''
@app.route('/health')
def health_check():
    """Endpoint de santé pour vérifier que le serveur fonctionne"""
    return jsonify({"status": "healthy", "port": 5008, "timestamp": datetime.now().isoformat()})
'''
    
    app_py_path = os.path.join(SERVER_PATH, "app.py")
    
    try:
        with open(app_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si l'endpoint existe déjà
        if '/health' not in content:
            # Ajouter l'endpoint avant la fin du fichier
            if 'if __name__ == "__main__":' in content:
                content = content.replace(
                    'if __name__ == "__main__":',
                    health_code + '\nif __name__ == "__main__":'
                )
            else:
                # Ajouter à la fin du fichier
                content += '\n' + health_code
                content += '\n\nif __name__ == "__main__":\n    app.run(host="0.0.0.0", port=5008, debug=False)\n'
            
            with open(app_py_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info("Endpoint de santé ajouté à app.py")
        
    except Exception as e:
        logger.warning(f"Impossible d'ajouter l'endpoint de santé: {e}")

def handle_native_message(message):
    """Traite un message Native Messaging"""
    try:
        request = json.loads(message)
        action = request.get("action")
        
        logger.info(f"Action reçue: {action}")
        
        if action == "start_server":
            return start_server()
        elif action == "check_server":
            return {"status": "running" if is_server_running() else "stopped"}
        else:
            return {"status": "error", "message": f"Action inconnue: {action}"}
            
    except json.JSONDecodeError as e:
        logger.error(f"Erreur JSON: {e}")
        return {"status": "error", "message": "JSON invalide"}
    except Exception as e:
        logger.error(f"Erreur lors du traitement: {e}")
        return {"status": "error", "message": str(e)}

def main():
    """Boucle principale Native Messaging"""
    logger.info("Démarrage du Native Messaging Host")
    
    # Ajouter l'endpoint de santé si nécessaire
    add_health_endpoint()
    
    try:
        while True:
            # Lire la longueur du message (4 bytes)
            raw_length = sys.stdin.buffer.read(4)
            if len(raw_length) == 0:
                logger.info("Fin de l'entrée, arrêt du programme")
                sys.exit(0)
            
            # Décoder la longueur
            message_length = int.from_bytes(raw_length, byteorder='little')
            
            # Lire le message
            message = sys.stdin.buffer.read(message_length).decode('utf-8')
            
            # Traiter le message
            response = handle_native_message(message)
            
            # Encoder et envoyer la réponse
            json_response = json.dumps(response).encode('utf-8')
            response_length = len(json_response).to_bytes(4, 'little')
            
            sys.stdout.buffer.write(response_length + json_response)
            sys.stdout.buffer.flush()
            
            logger.info(f"Réponse envoyée: {response}")
            
    except KeyboardInterrupt:
        logger.info("Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()