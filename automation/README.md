# 🚀 Memobrik - Système d'Automatisation Complet

## 📋 Vue d'ensemble

Ce système d'automatisation en **3 volets** permet de démarrer automatiquement le serveur Memobrik depuis Chrome et de gérer son cycle de vie de manière transparente.

### 🎯 Objectifs
- ✅ Démarrage automatique du serveur depuis Chrome
- ✅ Ouverture automatique du side panel
- ✅ Surveillance et diagnostic avancés
- ✅ Démarrage automatique au boot Windows
- ✅ Robustesse et gestion d'erreurs

## 🏗️ Architecture - 3 Volets

### 📡 Volet 1 : Native Messaging (Solution Principale)

**Composants :**
- `server_host.py` : Native Messaging Host en Python
- `chrome_extension/` : Extension Chrome avec side panel
- `install_native_messaging.bat` : Installation automatique

**Fonctionnement :**
1. L'utilisateur clique sur l'icône de l'extension Chrome
2. L'extension communique avec le Native Messaging Host
3. Le host démarre le serveur Flask si nécessaire
4. L'extension ouvre le side panel avec Memobrik

### 🛡️ Volet 2 : Robustesse & UX

**Composants :**
- `health_check.py` : Système de surveillance avancé
- Diagnostic complet du système
- Gestion d'erreurs et retry automatique
- Logs détaillés et notifications

**Fonctionnalités :**
- Health-check avec timeout configurable
- Diagnostic des processus et ports
- Vérification des dépendances
- Recommandations automatiques

### 🖥️ Volet 3 : Auto-Start OS (Fallback)

**Composants :**
- `windows_task_scheduler.ps1` : Configuration Windows Task Scheduler
- Démarrage automatique à la connexion
- Scripts de maintenance

**Avantages :**
- Serveur toujours disponible
- Pas besoin d'intervention manuelle
- Fallback si Native Messaging échoue

## 📦 Installation

### 🔧 Prérequis
- Windows 10/11
- Python 3.7+
- Google Chrome
- Privilèges administrateur (pour l'installation)

### ⚡ Installation Automatique

```batch
# Exécuter en tant qu'administrateur
cd deuxieme_cerveau/automation
install_complete_automation.bat
```

### 🔍 Installation Manuelle

#### 1. Native Messaging Host
```batch
# Compiler et installer
python -m pip install pyinstaller requests psutil
pyinstaller --onefile --noconsole server_host.py
install_native_messaging.bat
```

#### 2. Extension Chrome
1. Ouvrir Chrome → `chrome://extensions/`
2. Activer "Mode développeur"
3. "Charger l'extension non empaquetée"
4. Sélectionner le dossier `chrome_extension/`
5. Noter l'ID de l'extension
6. Modifier `C:\Program Files\Memobrik\com.memobrik.server_starter.json`
7. Remplacer `EXTENSION_ID_PLACEHOLDER` par l'ID réel

#### 3. Démarrage Automatique Windows
```powershell
# Exécuter en tant qu'administrateur
powershell -ExecutionPolicy Bypass -File windows_task_scheduler.ps1 -Action install
```

## 🎮 Utilisation

### 🚀 Démarrage Normal
1. Cliquer sur l'icône Memobrik dans Chrome
2. Le serveur démarre automatiquement
3. Le side panel s'ouvre avec l'interface

### 🔧 Diagnostic et Maintenance
```batch
# Diagnostic complet
diagnostic_complet.bat

# Démarrage manuel
start_manual.bat

# Vérifier la tâche planifiée
powershell windows_task_scheduler.ps1 -Action status
```

### 🩺 Health Check Avancé
```python
# Diagnostic programmatique
python health_check.py

# Vérification rapide
python -c "from health_check import MemobrikHealthChecker; print(MemobrikHealthChecker().check_server_health())"
```

## 📊 Monitoring et Logs

### 📄 Fichiers de Log
- `server_host.log` : Logs du Native Messaging Host
- `health_check.log` : Logs du système de surveillance
- `startup.log` : Logs du démarrage automatique Windows
- `task_scheduler.log` : Logs de la tâche planifiée

### 🔍 Diagnostic Automatique
Le système génère automatiquement :
- Rapports de diagnostic JSON horodatés
- Recommandations de résolution de problèmes
- Alertes en cas de dysfonctionnement

## 🛠️ Configuration Avancée

### ⚙️ Variables d'Environnement
```python
# Dans server_host.py
SERVER_PORT = 5008
SERVER_PATH = r"G:\memobrik\deuxieme_cerveau"
MAX_STARTUP_TIME = 20  # secondes
```

### 🔧 Personnalisation Extension
```javascript
// Dans background.js
const SERVER_PORT = 5008;
const MAX_RETRY_ATTEMPTS = 3;
const NATIVE_HOST = 'com.memobrik.server_starter';
```

### 📅 Configuration Tâche Planifiée
```powershell
# Paramètres personnalisés
.\windows_task_scheduler.ps1 -Action install -ServerPath "C:\MonChemin" -TaskName "MonMemobrik"
```

## 🚨 Dépannage

### ❌ Problèmes Courants

#### Extension ne démarre pas le serveur
1. Vérifier l'ID de l'extension dans le manifest
2. Redémarrer Chrome
3. Vérifier les logs : `server_host.log`

#### Serveur ne répond pas
```batch
# Diagnostic complet
diagnostic_complet.bat

# Vérifier les processus
tasklist | findstr python
netstat -an | findstr 5008
```

#### Native Messaging ne fonctionne pas
1. Vérifier le registre Windows :
   ```
   HKCU\Software\Google\Chrome\NativeMessagingHosts\com.memobrik.server_starter
   ```
2. Vérifier le fichier manifest :
   ```
   C:\Program Files\Memobrik\com.memobrik.server_starter.json
   ```

#### Tâche planifiée ne démarre pas
```powershell
# Vérifier l'état
Get-ScheduledTask -TaskName "MemobrikAutoStart"

# Tester manuellement
Start-ScheduledTask -TaskName "MemobrikAutoStart"

# Voir les logs
Get-WinEvent -LogName "Microsoft-Windows-TaskScheduler/Operational" | Where-Object {$_.Message -like "*MemobrikAutoStart*"}
```

### 🔧 Commandes de Diagnostic

```batch
# Test complet du système
python health_check.py

# Vérifier Native Messaging
python server_host.py

# Test de l'extension (Console Chrome)
chrome.runtime.sendMessage({action: 'start_server'})

# Vérifier la tâche planifiée
powershell windows_task_scheduler.ps1 -Action test
```

## 🗑️ Désinstallation

### 🧹 Désinstallation Complète
```batch
# Script automatique
uninstall_automation.bat

# Ou manuellement :
powershell windows_task_scheduler.ps1 -Action uninstall
"C:\Program Files\Memobrik\uninstall.bat"
```

### 🔄 Réinstallation
```batch
# Désinstaller puis réinstaller
uninstall_automation.bat
install_complete_automation.bat
```

## 📈 Performances et Optimisation

### ⚡ Temps de Démarrage Typiques
- Native Messaging : 2-5 secondes
- Démarrage serveur : 5-10 secondes
- Ouverture side panel : 1-2 secondes

### 🎯 Optimisations Implémentées
- Cache des vérifications de santé
- Retry automatique avec backoff
- Démarrage en arrière-plan sans fenêtre
- Timeout configurables
- Logs rotatifs

## 🔒 Sécurité

### 🛡️ Mesures de Sécurité
- `allowed_origins` limité à l'extension
- Pas d'exécution avec privilèges admin
- Validation des entrées JSON
- CORS configuré dans Flask
- Logs sécurisés (pas de données sensibles)

### 🔐 Bonnes Pratiques
- Extension installée en mode développeur uniquement
- Native Messaging Host dans Program Files
- Tâche planifiée avec utilisateur courant
- Pas de stockage de mots de passe

## 📚 API et Intégration

### 🔌 Endpoints Disponibles
```http
GET /health                 # Health check
GET /                      # Interface principale
GET /all_notes            # Page de toutes les notes
POST /save/<category>     # Sauvegarder une note
GET /categories           # Liste des catégories
```

### 📡 Messages Native Messaging
```json
// Démarrer le serveur
{"action": "start_server"}

// Vérifier l'état
{"action": "check_server"}

// Réponses
{"status": "started", "port": 5008}
{"status": "already_running", "port": 5008}
{"status": "error", "message": "..."}
```

## 🤝 Contribution et Support

### 🐛 Signaler un Bug
1. Exécuter `diagnostic_complet.bat`
2. Joindre les logs générés
3. Décrire les étapes de reproduction

### 💡 Suggestions d'Amélioration
- Démarrage encore plus rapide
- Interface de configuration graphique
- Support d'autres navigateurs
- Synchronisation cloud

---

## 📄 Licence et Crédits

**Memobrik Automation System v1.0**
Développé pour optimiser l'expérience utilisateur Memobrik

*Inspiré par les meilleures pratiques de GPT-5, Grok-4 et Claude-3*