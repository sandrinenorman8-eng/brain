#!/usr/bin/env python3
"""
Volet 2 : Robustesse & UX - Health Check Avancé
Système de surveillance et diagnostic du serveur Memobrik
"""

import requests
import time
import json
import logging
import psutil
import os
from datetime import datetime
from pathlib import Path

# Configuration
SERVER_PORT = 5008
SERVER_URL = f"http://localhost:{SERVER_PORT}"
HEALTH_ENDPOINT = f"{SERVER_URL}/health"
LOG_FILE = Path(__file__).parent / "health_check.log"

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MemobrikHealthChecker:
    def __init__(self):
        self.server_port = SERVER_PORT
        self.server_url = SERVER_URL
        self.health_endpoint = HEALTH_ENDPOINT
        
    def check_port_availability(self):
        """Vérifie si le port est libre ou occupé"""
        try:
            for conn in psutil.net_connections():
                if conn.laddr.port == self.server_port:
                    return {
                        "available": False,
                        "pid": conn.pid,
                        "status": conn.status
                    }
            return {"available": True}
        except Exception as e:
            logger.error(f"Erreur vérification port: {e}")
            return {"available": None, "error": str(e)}
    
    def check_process_running(self):
        """Vérifie si un processus Python/Flask tourne sur le port"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and 'python' in proc.info['name'].lower():
                        cmdline = proc.info['cmdline'] or []
                        if any('app.py' in arg for arg in cmdline):
                            processes.append({
                                "pid": proc.info['pid'],
                                "name": proc.info['name'],
                                "cmdline": ' '.join(cmdline)
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return processes
        except Exception as e:
            logger.error(f"Erreur vérification processus: {e}")
            return []
    
    def check_server_health(self, timeout=5):
        """Vérifie la santé du serveur via HTTP"""
        try:
            response = requests.get(
                self.health_endpoint, 
                timeout=timeout,
                headers={'Cache-Control': 'no-cache'}
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return {
                        "healthy": True,
                        "response_time": response.elapsed.total_seconds(),
                        "data": data
                    }
                except json.JSONDecodeError:
                    return {
                        "healthy": True,
                        "response_time": response.elapsed.total_seconds(),
                        "data": {"raw_response": response.text}
                    }
            else:
                return {
                    "healthy": False,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds()
                }
                
        except requests.exceptions.ConnectionError:
            return {"healthy": False, "error": "Connection refused"}
        except requests.exceptions.Timeout:
            return {"healthy": False, "error": "Timeout"}
        except Exception as e:
            return {"healthy": False, "error": str(e)}
    
    def check_dependencies(self):
        """Vérifie les dépendances système"""
        dependencies = {}
        
        # Vérifier Python
        try:
            import sys
            dependencies["python"] = {
                "available": True,
                "version": sys.version,
                "executable": sys.executable
            }
        except Exception as e:
            dependencies["python"] = {"available": False, "error": str(e)}
        
        # Vérifier Flask
        try:
            import flask
            dependencies["flask"] = {
                "available": True,
                "version": flask.__version__
            }
        except ImportError:
            dependencies["flask"] = {"available": False, "error": "Not installed"}
        
        # Vérifier requests
        try:
            import requests
            dependencies["requests"] = {
                "available": True,
                "version": requests.__version__
            }
        except ImportError:
            dependencies["requests"] = {"available": False, "error": "Not installed"}
        
        return dependencies
    
    def check_file_system(self):
        """Vérifie l'état du système de fichiers"""
        server_path = Path("G:/memobrik/deuxieme_cerveau")
        
        checks = {
            "server_directory": {
                "exists": server_path.exists(),
                "path": str(server_path)
            },
            "app_py": {
                "exists": (server_path / "app.py").exists(),
                "path": str(server_path / "app.py")
            },
            "data_directory": {
                "exists": (server_path / "data").exists(),
                "path": str(server_path / "data")
            }
        }
        
        # Vérifier l'espace disque
        try:
            if server_path.exists():
                disk_usage = psutil.disk_usage(str(server_path))
                checks["disk_space"] = {
                    "total_gb": round(disk_usage.total / (1024**3), 2),
                    "free_gb": round(disk_usage.free / (1024**3), 2),
                    "used_percent": round((disk_usage.used / disk_usage.total) * 100, 2)
                }
        except Exception as e:
            checks["disk_space"] = {"error": str(e)}
        
        return checks
    
    async def wait_until_server_ready(self, timeout_ms=20000, check_interval=500):
        """Attend que le serveur soit prêt avec vérifications avancées"""
        start_time = time.time() * 1000
        timeout_seconds = timeout_ms / 1000
        check_interval_seconds = check_interval / 1000
        
        logger.info(f"Attente du serveur (timeout: {timeout_seconds}s)")
        
        while (time.time() * 1000 - start_time) < timeout_ms:
            # Vérification de base
            health = self.check_server_health(timeout=3)
            
            if health.get("healthy"):
                logger.info(f"✅ Serveur prêt en {time.time() * 1000 - start_time:.0f}ms")
                return True
            
            # Vérifications avancées en cas d'échec
            port_info = self.check_port_availability()
            processes = self.check_process_running()
            
            logger.info(f"Port {self.server_port}: {port_info}")
            if processes:
                logger.info(f"Processus Python trouvés: {len(processes)}")
            
            await asyncio.sleep(check_interval_seconds)
        
        logger.error(f"❌ Timeout après {timeout_ms}ms")
        return False
    
    def full_diagnostic(self):
        """Diagnostic complet du système"""
        logger.info("🔍 Diagnostic complet en cours...")
        
        diagnostic = {
            "timestamp": datetime.now().isoformat(),
            "server_health": self.check_server_health(),
            "port_status": self.check_port_availability(),
            "processes": self.check_process_running(),
            "dependencies": self.check_dependencies(),
            "file_system": self.check_file_system()
        }
        
        # Résumé du diagnostic
        is_healthy = diagnostic["server_health"].get("healthy", False)
        port_available = diagnostic["port_status"].get("available")
        processes_count = len(diagnostic["processes"])
        
        diagnostic["summary"] = {
            "status": "healthy" if is_healthy else "unhealthy",
            "server_responding": is_healthy,
            "port_occupied": not port_available if port_available is not None else None,
            "python_processes": processes_count,
            "recommendations": self._generate_recommendations(diagnostic)
        }
        
        return diagnostic
    
    def _generate_recommendations(self, diagnostic):
        """Génère des recommandations basées sur le diagnostic"""
        recommendations = []
        
        server_health = diagnostic["server_health"]
        port_status = diagnostic["port_status"]
        processes = diagnostic["processes"]
        dependencies = diagnostic["dependencies"]
        
        if not server_health.get("healthy"):
            if port_status.get("available"):
                recommendations.append("Le port est libre mais le serveur ne répond pas. Démarrer le serveur.")
            else:
                recommendations.append(f"Le port {self.server_port} est occupé. Vérifier le processus PID {port_status.get('pid')}")
        
        if not processes and not server_health.get("healthy"):
            recommendations.append("Aucun processus Python/Flask détecté. Le serveur doit être démarré.")
        
        if not dependencies.get("flask", {}).get("available"):
            recommendations.append("Flask n'est pas installé. Exécuter: pip install flask")
        
        if not dependencies.get("requests", {}).get("available"):
            recommendations.append("Requests n'est pas installé. Exécuter: pip install requests")
        
        fs_checks = diagnostic["file_system"]
        if not fs_checks.get("server_directory", {}).get("exists"):
            recommendations.append("Le répertoire du serveur n'existe pas. Vérifier le chemin G:/memobrik/deuxieme_cerveau")
        
        if not fs_checks.get("app_py", {}).get("exists"):
            recommendations.append("Le fichier app.py est manquant dans le répertoire du serveur")
        
        return recommendations

def main():
    """Fonction principale pour exécuter le diagnostic"""
    checker = MemobrikHealthChecker()
    
    # Diagnostic complet
    diagnostic = checker.full_diagnostic()
    
    # Affichage des résultats
    print("\n" + "="*60)
    print("🏥 DIAGNOSTIC MEMOBRIK HEALTH CHECK")
    print("="*60)
    
    summary = diagnostic["summary"]
    status_emoji = "✅" if summary["status"] == "healthy" else "❌"
    print(f"\n{status_emoji} État général: {summary['status'].upper()}")
    
    if summary["server_responding"]:
        response_time = diagnostic["server_health"].get("response_time", 0)
        print(f"🌐 Serveur: Répond en {response_time:.3f}s")
    else:
        print("🌐 Serveur: Non accessible")
    
    if summary["port_occupied"] is not None:
        port_emoji = "🔒" if summary["port_occupied"] else "🔓"
        print(f"{port_emoji} Port {checker.server_port}: {'Occupé' if summary['port_occupied'] else 'Libre'}")
    
    print(f"🐍 Processus Python: {summary['python_processes']} trouvé(s)")
    
    # Recommandations
    if summary["recommendations"]:
        print(f"\n💡 RECOMMANDATIONS:")
        for i, rec in enumerate(summary["recommendations"], 1):
            print(f"   {i}. {rec}")
    
    # Sauvegarder le diagnostic
    diagnostic_file = Path(__file__).parent / f"diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(diagnostic_file, 'w', encoding='utf-8') as f:
        json.dump(diagnostic, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Diagnostic sauvegardé: {diagnostic_file}")
    print("="*60)
    
    return diagnostic

if __name__ == "__main__":
    import asyncio
    main()