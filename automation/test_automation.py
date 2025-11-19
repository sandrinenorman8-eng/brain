#!/usr/bin/env python3
"""
Script de test pour vérifier le système d'automatisation Memobrik
Tests des 3 volets : Native Messaging + Robustesse + Auto-Start OS
"""

import sys
import os
import json
import time
import subprocess
import requests
from pathlib import Path
from health_check import MemobrikHealthChecker

class MemobrikAutomationTester:
    def __init__(self):
        self.checker = MemobrikHealthChecker()
        self.test_results = []
        
    def log_test(self, test_name, success, message="", details=None):
        """Enregistre le résultat d'un test"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details or {}
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if details and not success:
            for key, value in details.items():
                print(f"    {key}: {value}")
    
    def test_python_dependencies(self):
        """Test 1: Vérifier les dépendances Python"""
        try:
            dependencies = self.checker.check_dependencies()
            
            required_deps = ["python", "flask", "requests"]
            missing_deps = []
            
            for dep in required_deps:
                if not dependencies.get(dep, {}).get("available", False):
                    missing_deps.append(dep)
            
            if missing_deps:
                self.log_test(
                    "Dépendances Python",
                    False,
                    f"Dépendances manquantes: {', '.join(missing_deps)}",
                    dependencies
                )
            else:
                self.log_test(
                    "Dépendances Python",
                    True,
                    "Toutes les dépendances sont disponibles"
                )
                
        except Exception as e:
            self.log_test("Dépendances Python", False, f"Erreur: {e}")
    
    def test_file_system(self):
        """Test 2: Vérifier le système de fichiers"""
        try:
            fs_checks = self.checker.check_file_system()
            
            critical_files = ["server_directory", "app_py"]
            missing_files = []
            
            for file_check in critical_files:
                if not fs_checks.get(file_check, {}).get("exists", False):
                    missing_files.append(file_check)
            
            if missing_files:
                self.log_test(
                    "Système de fichiers",
                    False,
                    f"Fichiers manquants: {', '.join(missing_files)}",
                    fs_checks
                )
            else:
                self.log_test(
                    "Système de fichiers",
                    True,
                    "Tous les fichiers critiques sont présents"
                )
                
        except Exception as e:
            self.log_test("Système de fichiers", False, f"Erreur: {e}")
    
    def test_native_messaging_host(self):
        """Test 3: Vérifier le Native Messaging Host"""
        try:
            # Vérifier que l'exécutable existe
            host_path = Path("C:/Program Files/Memobrik/server_host.exe")
            
            if not host_path.exists():
                self.log_test(
                    "Native Messaging Host",
                    False,
                    "Exécutable non trouvé",
                    {"path": str(host_path)}
                )
                return
            
            # Vérifier le manifest
            manifest_path = Path("C:/Program Files/Memobrik/com.memobrik.server_starter.json")
            
            if not manifest_path.exists():
                self.log_test(
                    "Native Messaging Host",
                    False,
                    "Manifest non trouvé",
                    {"path": str(manifest_path)}
                )
                return
            
            # Vérifier le contenu du manifest
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            required_fields = ["name", "description", "path", "type", "allowed_origins"]
            missing_fields = [field for field in required_fields if field not in manifest]
            
            if missing_fields:
                self.log_test(
                    "Native Messaging Host",
                    False,
                    f"Champs manquants dans le manifest: {', '.join(missing_fields)}",
                    manifest
                )
            else:
                self.log_test(
                    "Native Messaging Host",
                    True,
                    "Native Messaging Host correctement installé"
                )
                
        except Exception as e:
            self.log_test("Native Messaging Host", False, f"Erreur: {e}")
    
    def test_server_startup(self):
        """Test 4: Tester le démarrage du serveur"""
        try:
            # Vérifier si le serveur est déjà en cours
            initial_health = self.checker.check_server_health()
            
            if initial_health.get("healthy"):
                self.log_test(
                    "Démarrage serveur",
                    True,
                    "Serveur déjà en cours d'exécution"
                )
                return
            
            # Essayer de démarrer le serveur via le script
            server_path = Path("G:/memobrik/deuxieme_cerveau")
            start_script = server_path / "START.bat"
            
            if not start_script.exists():
                self.log_test(
                    "Démarrage serveur",
                    False,
                    "Script de démarrage non trouvé",
                    {"path": str(start_script)}
                )
                return
            
            print("    Démarrage du serveur en cours...")
            
            # Démarrer le serveur en arrière-plan
            process = subprocess.Popen(
                [str(start_script)],
                cwd=str(server_path),
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Attendre que le serveur soit prêt
            max_wait = 30
            for i in range(max_wait):
                time.sleep(1)
                health = self.checker.check_server_health()
                
                if health.get("healthy"):
                    self.log_test(
                        "Démarrage serveur",
                        True,
                        f"Serveur démarré en {i+1} secondes"
                    )
                    return
                
                print(f"    Attente... {i+1}/{max_wait}s")
            
            self.log_test(
                "Démarrage serveur",
                False,
                f"Timeout après {max_wait} secondes"
            )
            
        except Exception as e:
            self.log_test("Démarrage serveur", False, f"Erreur: {e}")
    
    def test_health_endpoint(self):
        """Test 5: Tester l'endpoint de santé"""
        try:
            health = self.checker.check_server_health(timeout=10)
            
            if health.get("healthy"):
                response_time = health.get("response_time", 0)
                data = health.get("data", {})
                
                self.log_test(
                    "Endpoint de santé",
                    True,
                    f"Réponse en {response_time:.3f}s",
                    data
                )
            else:
                self.log_test(
                    "Endpoint de santé",
                    False,
                    "Serveur ne répond pas",
                    health
                )
                
        except Exception as e:
            self.log_test("Endpoint de santé", False, f"Erreur: {e}")
    
    def test_scheduled_task(self):
        """Test 6: Vérifier la tâche planifiée Windows"""
        try:
            # Exécuter la commande PowerShell pour vérifier la tâche
            cmd = [
                "powershell", "-ExecutionPolicy", "Bypass", "-Command",
                "Get-ScheduledTask -TaskName 'MemobrikAutoStart' -ErrorAction SilentlyContinue | ConvertTo-Json"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                try:
                    task_info = json.loads(result.stdout)
                    self.log_test(
                        "Tâche planifiée",
                        True,
                        f"Tâche trouvée - État: {task_info.get('State', 'Unknown')}",
                        {"task_name": task_info.get("TaskName"), "state": task_info.get("State")}
                    )
                except json.JSONDecodeError:
                    self.log_test(
                        "Tâche planifiée",
                        True,
                        "Tâche trouvée (format non-JSON)"
                    )
            else:
                self.log_test(
                    "Tâche planifiée",
                    False,
                    "Tâche 'MemobrikAutoStart' non trouvée"
                )
                
        except subprocess.TimeoutExpired:
            self.log_test("Tâche planifiée", False, "Timeout PowerShell")
        except Exception as e:
            self.log_test("Tâche planifiée", False, f"Erreur: {e}")
    
    def test_chrome_extension_files(self):
        """Test 7: Vérifier les fichiers de l'extension Chrome"""
        try:
            extension_path = Path(__file__).parent / "chrome_extension"
            
            required_files = [
                "manifest.json",
                "background.js",
                "sidepanel.html"
            ]
            
            missing_files = []
            for file_name in required_files:
                file_path = extension_path / file_name
                if not file_path.exists():
                    missing_files.append(file_name)
            
            if missing_files:
                self.log_test(
                    "Extension Chrome",
                    False,
                    f"Fichiers manquants: {', '.join(missing_files)}",
                    {"extension_path": str(extension_path)}
                )
            else:
                # Vérifier le manifest
                manifest_path = extension_path / "manifest.json"
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                
                self.log_test(
                    "Extension Chrome",
                    True,
                    f"Extension v{manifest.get('version', 'unknown')} prête",
                    {"name": manifest.get("name"), "version": manifest.get("version")}
                )
                
        except Exception as e:
            self.log_test("Extension Chrome", False, f"Erreur: {e}")
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🧪 TESTS DU SYSTÈME D'AUTOMATISATION MEMOBRIK")
        print("=" * 60)
        print()
        
        # Exécuter tous les tests
        self.test_python_dependencies()
        self.test_file_system()
        self.test_native_messaging_host()
        self.test_chrome_extension_files()
        self.test_server_startup()
        self.test_health_endpoint()
        self.test_scheduled_task()
        
        # Résumé des résultats
        print()
        print("=" * 60)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total: {total_tests} tests")
        print(f"✅ Réussis: {passed_tests}")
        print(f"❌ Échoués: {failed_tests}")
        print(f"📈 Taux de réussite: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print()
            print("❌ TESTS ÉCHOUÉS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   - {result['test']}: {result['message']}")
        
        # Sauvegarder les résultats
        results_file = Path(__file__).parent / f"test_results_{int(time.time())}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": time.time(),
                "summary": {
                    "total": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "success_rate": (passed_tests/total_tests)*100
                },
                "tests": self.test_results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Résultats sauvegardés: {results_file}")
        
        return failed_tests == 0

def main():
    """Fonction principale"""
    tester = MemobrikAutomationTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print("Le système d'automatisation est prêt à être utilisé.")
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Consultez les détails ci-dessus pour résoudre les problèmes.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())