# 🚀 Guide Rapide - Memobrik Automation

## ⚡ Installation Express (5 minutes)

### 1️⃣ Installation Automatique
```batch
# Clic droit → "Exécuter en tant qu'administrateur"
install_complete_automation.bat
```

### 2️⃣ Installer l'Extension Chrome
1. Ouvrir Chrome → `chrome://extensions/`
2. Activer "Mode développeur" (coin supérieur droit)
3. Cliquer "Charger l'extension non empaquetée"
4. Sélectionner le dossier : `deuxieme_cerveau/automation/chrome_extension/`

### 3️⃣ Configurer l'Extension
1. **Noter l'ID de l'extension** affiché dans Chrome
2. Ouvrir le fichier : `C:\Program Files\Memobrik\com.memobrik.server_starter.json`
3. Remplacer `EXTENSION_ID_PLACEHOLDER` par l'ID réel
4. Sauvegarder et redémarrer Chrome

### 4️⃣ Test Final
1. Cliquer sur l'icône Memobrik dans Chrome
2. Le serveur démarre automatiquement
3. Le side panel s'ouvre avec Memobrik

## 🎯 Utilisation Quotidienne

### Démarrage Normal
- **Clic sur l'icône** → Serveur démarre → Side panel s'ouvre
- **Temps total** : 5-10 secondes

### Démarrage Automatique
- Le serveur démarre automatiquement à la connexion Windows
- Plus besoin d'intervention manuelle

## 🔧 Dépannage Express

### ❌ Extension ne fonctionne pas
```batch
# Diagnostic rapide
diagnostic_complet.bat
```

### ❌ Serveur ne démarre pas
```batch
# Démarrage manuel
start_manual.bat
```

### ❌ Problème de configuration
```batch
# Test complet
python test_automation.py
```

## 📞 Support Rapide

### Commandes Utiles
```batch
# Diagnostic complet
diagnostic_complet.bat

# Test du système
python test_automation.py

# Redémarrer les services
STOP.bat
START.bat

# Désinstaller l'automation
uninstall_automation.bat
```

### Logs Importants
- `server_host.log` : Native Messaging
- `health_check.log` : Surveillance
- `startup.log` : Démarrage auto Windows

---

## ✅ Checklist de Vérification

- [ ] Installation automatique terminée sans erreur
- [ ] Extension Chrome installée et ID configuré
- [ ] Clic sur l'icône démarre le serveur
- [ ] Side panel s'ouvre automatiquement
- [ ] Diagnostic complet sans erreur
- [ ] Démarrage automatique Windows configuré

**🎉 Si tous les points sont cochés, votre système est opérationnel !**