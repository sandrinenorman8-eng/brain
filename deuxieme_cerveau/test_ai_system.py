# -*- coding: utf-8 -*-
"""
Test rapide du système de Fusion Intelligente
"""

import sys
import os

# Ajouter le dossier au path
sys.path.insert(0, os.path.dirname(__file__))

from services.ai_service import AIService

def test_ai_connection():
    """Teste la connexion à l'API IA"""
    print("🧪 Test de connexion à l'API IA...")
    
    ai_service = AIService()
    is_connected = ai_service.test_connection()
    
    if is_connected:
        print("✅ API IA connectée avec succès !")
        return True
    else:
        print("❌ Impossible de se connecter à l'API IA")
        return False

def test_ai_organization():
    """Teste l'organisation d'un texte simple"""
    print("\n🧪 Test d'organisation de texte...")
    
    ai_service = AIService()
    
    # Texte de test
    test_content = """
10:30:15: Faire la présentation pour le client
11:45:22: Appeler Jean pour discuter du projet
14:20:00: Réunion équipe - décisions importantes sur l'architecture
15:30:00: Corriger le bug dans le module de recherche
16:00:00: Mettre à jour la documentation
"""
    
    result = ai_service.organize_fusion(test_content, "Test")
    
    if result['success']:
        print("✅ Organisation réussie !")
        print("\n📝 Résultat organisé :")
        print("-" * 60)
        print(result['organized_content'])
        print("-" * 60)
        return True
    else:
        print(f"❌ Erreur d'organisation : {result.get('error')}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🧠 TEST DU SYSTÈME DE FUSION INTELLIGENTE")
    print("=" * 60)
    
    # Test 1 : Connexion
    connection_ok = test_ai_connection()
    
    if connection_ok:
        # Test 2 : Organisation
        organization_ok = test_ai_organization()
        
        if organization_ok:
            print("\n" + "=" * 60)
            print("✅ TOUS LES TESTS SONT PASSÉS !")
            print("=" * 60)
            print("\n💡 Le système est prêt à être utilisé :")
            print("   1. Démarrez l'application : START.bat")
            print("   2. Ouvrez : http://localhost:5008")
            print("   3. Cliquez sur '🧠 Fusion IA'")
        else:
            print("\n❌ Le test d'organisation a échoué")
    else:
        print("\n❌ Impossible de se connecter à l'API")
        print("\n💡 Vérifiez :")
        print("   - Votre connexion internet")
        print("   - La clé API dans config.ini")
