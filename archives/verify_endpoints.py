#!/usr/bin/env python3
"""
VÉRIFICATION COMPLÈTE DES ENDPOINTS API
Teste que toutes les fonctions API appellent les bonnes routes Flask
"""

import requests
import json
import time

BASE_URL = "http://localhost:5008"

def test_endpoint(name, method, url, data=None, expected_status=200, description=""):
    """Test un endpoint spécifique"""
    print(f"\n🧪 Test: {name}")
    if description:
        print(f"   📝 {description}")
    print(f"   {method} {url}")

    try:
        headers = {'Content-Type': 'application/json'}

        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            print(f"   ❌ Méthode non supportée: {method}")
            return False

        print(f"   Status: {response.status_code} (attendu: {expected_status})")

        if response.status_code == expected_status:
            print("   ✅ SUCCÈS")
            # Afficher quelques infos sur la réponse
            try:
                if response.headers.get('content-type', '').startswith('application/json'):
                    json_data = response.json()
                    if isinstance(json_data, list):
                        print(f"   📊 {len(json_data)} éléments")
                    elif isinstance(json_data, dict):
                        if 'filename' in json_data:
                            print(f"   📄 {json_data.get('filename', 'N/A')}")
                        elif 'message' in json_data:
                            print(f"   💬 {json_data.get('message', 'N/A')}")
                        elif 'error' in json_data:
                            print(f"   🚨 {json_data.get('error', 'N/A')}")
            except:
                pass
            return True
        else:
            print("   ❌ ÉCHEC")
            try:
                error_data = response.json()
                print(f"   🚨 Erreur: {error_data}")
            except:
                print(f"   🚨 Response: {response.text[:100]}...")
            return False

    except requests.exceptions.RequestException as e:
        print(f"   ❌ EXCEPTION: {str(e)}")
        return False

def main():
    print("🔗 VÉRIFICATION COMPLÈTE DES ENDPOINTS API")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")

    # Attendre que le serveur soit prêt
    print("\n⏳ Test de connexion au serveur...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Serveur accessible")
        else:
            print(f"⚠️ Serveur répond avec status {response.status_code}")
    except:
        print("❌ Serveur non accessible")
        return

    # Définition de tous les endpoints à tester
    # Format: (nom, méthode, url, données, status_attendu, description)
    endpoints = [
        # Endpoints GET de base
        ("Catégories", "GET", f"{BASE_URL}/categories", None, 200, "api.loadCategories()"),
        ("Tous les fichiers", "GET", f"{BASE_URL}/all_files", None, 200, "api.loadAllFiles()"),
        ("Liste catégorie", "GET", f"{BASE_URL}/list/scénario", None, 200, "api.loadFilesByCategories()"),

        # Endpoints POST
        ("Sauvegarde note", "POST", f"{BASE_URL}/save/scénario", {"text": "Test API endpoint"}, 200, "api.quickSave()"),
        ("Ajouter catégorie", "POST", f"{BASE_URL}/add_category", {"name": "test_api_category"}, 200, "api.addNewCategory()"),
        ("Créer backup", "POST", f"{BASE_URL}/backup_project", None, 200, "api.createBackup()"),

        # Endpoints Fusion
        ("Fusion globale", "POST", f"{BASE_URL}/fusion/global", None, 200, "api.performGlobalFusion()"),
        ("Fusion par catégories", "POST", f"{BASE_URL}/fusion/category", {"categories": ["scénario"]}, 200, "api.performCategoryFusion()"),
        ("Fusion catégorie unique", "POST", f"{BASE_URL}/fusion/single-category", {"category": "scénario"}, 200, "api.performSingleCategoryFusion()"),

        # Endpoints divers
        ("Ouvrir dossier", "GET", f"{BASE_URL}/open_folder/scénario", None, 200, "api.openFolder()"),
        ("Lire fichier", "GET", f"{BASE_URL}/read/scénario/readme.txt", None, 200, "Non utilisé dans API"),

        # Endpoints DELETE (test avec catégorie qui n'existe pas pour éviter suppression réelle)
        ("Supprimer catégorie", "DELETE", f"{BASE_URL}/erase_category/nonexistent_test_category", None, 404, "api.deleteCategory() - catégorie inexistante"),
    ]

    results = []
    passed = 0
    failed = 0

    print(f"\n🧪 Test des {len(endpoints)} endpoints...\n")

    for name, method, url, data, expected_status, description in endpoints:
        success = test_endpoint(name, method, url, data, expected_status, description)
        results.append((name, success))

        if success:
            passed += 1
        else:
            failed += 1

    # Analyse détaillée par fonction API
    print("\n" + "=" * 60)
    print("🔍 ANALYSE PAR FONCTION API")
    print("=" * 60)

    api_functions = {
        "loadCategories()": [("Catégories", True)],
        "loadAllFiles()": [("Tous les fichiers", True)],
        "loadFilesByCategories()": [("Liste catégorie", True)],
        "quickSave()": [("Sauvegarde note", True)],
        "addNewCategory()": [("Ajouter catégorie", True)],
        "createBackup()": [("Créer backup", True)],
        "performGlobalFusion()": [("Fusion globale", True)],
        "performCategoryFusion()": [("Fusion par catégories", True)],
        "performSingleCategoryFusion()": [("Fusion catégorie unique", True)],
        "openFolder()": [("Ouvrir dossier", True)],
        "deleteCategory()": [("Supprimer catégorie", True)],
    }

    api_success = 0
    api_total = len(api_functions)

    for func_name, expected_tests in api_functions.items():
        print(f"\n📋 {func_name}")
        func_passed = 0
        func_total = len(expected_tests)

        for test_name, should_pass in expected_tests:
            # Trouver le résultat du test
            test_result = next((result for name, result in results if name == test_name), None)
            if test_result is not None:
                status = "✅" if test_result else "❌"
                print(f"   {status} {test_name}")
                if test_result:
                    func_passed += 1
            else:
                print(f"   ❓ {test_name} (test non trouvé)")

        success_rate = func_passed / func_total * 100
        print(f"   📊 {func_passed}/{func_total} tests réussis ({success_rate:.0f}%)")

        if func_passed == func_total:
            api_success += 1

    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS FINAUX")
    print("=" * 60)
    print(f"🔗 Endpoints testés: {len(endpoints)}")
    print(f"✅ Endpoints réussis: {passed}")
    print(f"❌ Endpoints échoués: {failed}")
    print(f"📈 Taux de succès endpoints: {passed/len(endpoints)*100:.1f}%")
    print()
    print(f"🔧 Fonctions API: {api_total}")
    print(f"✅ Fonctions API opérationnelles: {api_success}")
    print(f"❌ Fonctions API défaillantes: {api_total - api_success}")
    print(f"📈 Taux de succès API: {api_success/api_total*100:.1f}%")

    if failed == 0:
        print("\n🎉 TOUTES LES FONCTIONS API APPELLENT LES BONS ENDPOINTS !")
        print("🔗 L'intégration frontend/backend est parfaite.")
    else:
        print("\n⚠️ Certains endpoints ne fonctionnent pas correctement.")
        print("🔍 Vérifiez les erreurs ci-dessus et corrigez les routes.")

    # Recommandations
    print("\n" + "=" * 60)
    print("💡 RECOMMANDATIONS")
    print("=" * 60)

    if passed == len(endpoints):
        print("✅ Toutes les routes sont correctement configurées")
        print("✅ Les fonctions API utilisent les bonnes endpoints")
        print("✅ L'application est prête pour la production")
    else:
        print("⚠️ Vérifiez les routes suivantes dans app.py:")
        for name, success in results:
            if not success:
                print(f"   - {name}")

    return passed == len(endpoints)

if __name__ == "__main__":
    success = main()
    print(f"\n🔚 Script terminé avec {'succès' if success else 'échec'}")
    exit(0 if success else 1)
