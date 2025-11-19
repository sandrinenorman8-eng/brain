#!/usr/bin/env python3
"""
Test de connectivité réseau pour l'application Deuxième Cerveau
"""

import socket
import requests

def check_port(port):
    """Vérifie si un port est ouvert"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    print('🔍 Vérification du réseau - Deuxième Cerveau')
    print('=' * 50)

    # Vérifier le port 5008 uniquement
    port = 5008
    print('📡 État du port:')
    is_open = check_port(port)
    status = '🟢 ACTIF' if is_open else '🔴 INACTIF'
    print(f'   Port {port}: {status}')

    print('\n🌐 Test de connectivité HTTP (localhost):')
    print('-' * 40)

    # Tester l'accès HTTP
    try:
        response = requests.get(f'http://localhost:{port}/', timeout=3)
        print(f'   ✅ localhost:{port} - HTTP {response.status_code} - {len(response.text)} octets')
    except Exception as e:
        print(f'   ❌ localhost:{port} - Connexion échouée: {str(e)[:50]}...')

    print('\n🌍 Test d\'accès réseau (127.0.0.1):')
    print('-' * 35)

    try:
        response = requests.get(f'http://127.0.0.1:{port}/', timeout=3)
        print(f'   ✅ 127.0.0.1:{port} - HTTP {response.status_code}')
    except Exception as e:
        print(f'   ❌ 127.0.0.1:{port} - {str(e)[:50]}...')

    # Obtenir l'adresse IP locale
    print('\n🏠 Détection de l\'adresse IP réseau:')
    print('-' * 35)

    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f'   📍 Adresse IP locale: {local_ip}')

        # Tester l'accès réseau avec l'IP locale
        print('\n🌐 Test d\'accès réseau (IP locale):')
        print('-' * 30)

        try:
            response = requests.get(f'http://{local_ip}:{port}/', timeout=3)
            print(f'   ✅ {local_ip}:{port} - HTTP {response.status_code}')
        except Exception as e:
            print(f'   ❌ {local_ip}:{port} - {str(e)[:50]}...')

    except Exception as e:
        print(f'   ❌ Impossible de détecter l\'IP locale: {e}')

    print('\n📋 Résumé:')
    print('-' * 10)
    print('🟢 Port 5008 devrait être ACTIF si l\'app Flask fonctionne')
    print('🌐 L\'app devrait être accessible sur le réseau local')
    print('💡 Utilise l\'IP locale + :5008 pour accéder depuis d\'autres appareils')
    print('🎯 Port standardisé: 5008 uniquement')

if __name__ == "__main__":
    main()
