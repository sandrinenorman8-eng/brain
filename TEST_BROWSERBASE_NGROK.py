# -*- coding: utf-8 -*-
"""
Test Browserbase MCP avec ngrok URL
Teste l'accès à l'app Flask via tunnel ngrok
"""

import subprocess
import time
import requests
import json

def start_ngrok(port=5008):
    """Démarre ngrok sur le port Flask"""
    print(f"\n[1/4] Démarrage ngrok sur port {port}...")
    
    # Lancer ngrok en arrière-plan
    process = subprocess.Popen(
        ['ngrok.exe', 'http', str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Attendre que ngrok démarre
    time.sleep(3)
    
    # Récupérer l'URL publique
    try:
        response = requests.get('http://localhost:4040/api/tunnels')
        tunnels = response.json()['tunnels']
        
        for tunnel in tunnels:
            if tunnel['proto'] == 'https':
                public_url = tunnel['public_url']
                print(f"✅ Ngrok URL: {public_url}")
                return process, public_url
    except Exception as e:
        print(f"❌ Erreur récupération URL ngrok: {e}")
        return process, None

def test_flask_local():
    """Teste si Flask tourne localement"""
    print("\n[2/4] Test Flask local...")
    
    try:
        r = requests.get('http://localhost:5008/categories', timeout=5)
        if r.status_code == 200:
            print(f"✅ Flask OK - {len(r.json())} catégories")
            return True
        else:
            print(f"⚠️ Flask répond mais status {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ Flask non accessible: {e}")
        return False

def test_ngrok_access(ngrok_url):
    """Teste l'accès via ngrok"""
    print("\n[3/4] Test accès via ngrok...")
    
    if not ngrok_url:
        print("❌ Pas d'URL ngrok")
        return False
    
    try:
        r = requests.get(f"{ngrok_url}/categories", timeout=10)
        if r.status_code == 200:
            print(f"✅ Ngrok OK - {len(r.json())} catégories")
            return True
        else:
            print(f"⚠️ Ngrok répond mais status {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ngrok non accessible: {e}")
        return False

def create_browserbase_test_prompt(ngrok_url):
    """Crée le prompt pour tester avec Browserbase MCP"""
    print("\n[4/4] Instructions test Browserbase MCP...")
    
    prompt = f"""
=== TEST BROWSERBASE MCP ===

URL de l'application: {ngrok_url}

PROMPT À UTILISER DANS KIRO:

"Utilise Browserbase MCP pour:
1. Naviguer vers {ngrok_url}
2. Prendre un screenshot de la page d'accueil
3. Cliquer sur le bouton 'Fusion IA'
4. Observer les éléments de la page fusion intelligente
5. Extraire le texte du statut API
6. Me donner un résumé de ce que tu vois"

COMMANDES MCP DISPONIBLES:
- browserbase_stagehand_navigate: Naviguer vers URL
- browserbase_stagehand_observe: Observer éléments page
- browserbase_stagehand_act: Interagir (clic, remplir)
- browserbase_stagehand_extract: Extraire données
- browserbase_screenshot: Prendre screenshot

EXEMPLE DIRECT:
Demande à Kiro: "Navigate to {ngrok_url} using browserbase and take a screenshot"
"""
    
    print(prompt)
    
    # Sauvegarder dans fichier
    with open('BROWSERBASE_TEST_INSTRUCTIONS.txt', 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print("\n✅ Instructions sauvegardées dans: BROWSERBASE_TEST_INSTRUCTIONS.txt")
    return prompt

def main():
    print("=" * 60)
    print("TEST BROWSERBASE MCP AVEC NGROK")
    print("=" * 60)
    
    # Vérifier Flask
    if not test_flask_local():
        print("\n⚠️ Flask doit tourner sur port 5008")
        print("Lancer: START_ALL_SERVICES.bat ou python deuxieme_cerveau/app.py")
        return
    
    # Démarrer ngrok
    ngrok_process, ngrok_url = start_ngrok(5008)
    
    if not ngrok_url:
        print("\n❌ Impossible de démarrer ngrok")
        print("Vérifier que ngrok.exe est dans le PATH")
        return
    
    # Tester accès ngrok
    if not test_ngrok_access(ngrok_url):
        print("\n❌ Ngrok ne fonctionne pas correctement")
        ngrok_process.terminate()
        return
    
    # Créer instructions test
    create_browserbase_test_prompt(ngrok_url)
    
    print("\n" + "=" * 60)
    print("PRÊT POUR TEST BROWSERBASE")
    print("=" * 60)
    print(f"\n📍 URL publique: {ngrok_url}")
    print("\n🔧 Copie le prompt ci-dessus dans Kiro")
    print("\n⚠️ Appuie sur ENTER pour arrêter ngrok...")
    
    input()
    
    # Arrêter ngrok
    print("\n[STOP] Arrêt ngrok...")
    ngrok_process.terminate()
    print("✅ Terminé")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[STOP] Interruption utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
