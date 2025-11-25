# 🚨 GUIDE DE DÉMARRAGE D'URGENCE

## SI TOUT EST CASSÉ - PROCÉDURE DE RÉCUPÉRATION

### ✅ ÉTAPE 1 : VÉRIFIER LES FICHIERS CRITIQUES

Ces fichiers DOIVENT exister :
```
deuxieme_cerveau/
├── app_new.py                    ✓ Application principale
├── category_path_resolver.py     ✓ Résolution chemins
├── categories.json               ✓ Définition catégories
├── category_mapping.json         ✓ Mapping hiérarchique
├── search-server-fixed.js        ✓ Serveur recherche
├── index.html                    ✓ Interface
└── data/                         ✓ TOUTES VOS NOTES
```

**Commande de vérification** :
```bash
cd deuxieme_cerveau
dir app_new.py category_path_resolver.py categories.json category_mapping.json search-server-fixed.js index.html
```

---

### ✅ ÉTAPE 2 : RÉINSTALLER LES DÉPENDANCES

```bash
cd deuxieme_cerveau

# Python
pip install -r requirements.txt

# Vérifier installation
python -c "import flask; print('Flask OK')"
python -c "import requests; print('Requests OK')"
```

**Dépendances requises** :
- Flask==3.0.0
- requests==2.32.3
- python-dotenv==1.0.0

---

### ✅ ÉTAPE 3 : DÉMARRAGE MANUEL

#### Option A : Script automatique
```bash
cd deuxieme_cerveau
START.bat
```

#### Option B : Démarrage manuel (si START.bat ne fonctionne pas)

**Terminal 1 - Flask** :
```bash
cd deuxieme_cerveau
python app_new.py
```

**Terminal 2 - Node.js** :
```bash
cd deuxieme_cerveau
node search-server-fixed.js
```

---

### ✅ ÉTAPE 4 : VÉRIFIER QUE ÇA FONCTIONNE

1. **Ouvrir navigateur** : http://localhost:5008
2. **Vérifier Flask** : Doit afficher l'interface
3. **Vérifier Node.js** : http://localhost:3008/status
   - Doit retourner : `{"status":"ok","service":"search-server","port":3008}`

---

## 🔧 PROBLÈMES COURANTS

### Problème : "Port 5008 already in use"
**Solution** :
```bash
# Windows
netstat -ano | findstr :5008
taskkill /PID <PID> /F

# Ou changer le port dans config/config.py
PORT = 5009
```

### Problème : "Module 'flask' not found"
**Solution** :
```bash
pip install flask==3.0.0
```

### Problème : "Cannot find module 'fs'"
**Solution** : Node.js mal installé
```bash
# Télécharger Node.js : https://nodejs.org/
# Version recommandée : 18.x ou 20.x
node --version
```

### Problème : "categories.json not found"
**Solution** : Recréer le fichier
```json
{
  "todo": {"emoji": "✅", "color": "#4CAF50"},
  "memobrik": {"emoji": "🧠", "color": "#2196F3"}
}
```

### Problème : "category_mapping.json not found"
**Solution** : Recréer le fichier
```json
{
  "todo": "priorité/todo",
  "memobrik": "logiciels/memobrik"
}
```

### Problème : Encodage bizarre dans les notes
**Solution** : Les fichiers sont en UTF-8
```bash
# Convertir fichier en UTF-8
python -c "
import sys
with open('fichier.txt', 'r', encoding='cp1252') as f:
    content = f.read()
with open('fichier.txt', 'w', encoding='utf-8') as f:
    f.write(content)
"
```

---

## 💾 RÉCUPÉRATION DE DONNÉES

### Si le dossier data/ est corrompu

1. **Chercher les backups** :
```bash
dir zip\*.zip
```

2. **Extraire le dernier backup** :
```bash
# Extraire dans un dossier temporaire
# Copier le dossier data/ vers deuxieme_cerveau/
```

3. **Vérifier l'intégrité** :
```bash
cd deuxieme_cerveau
python -c "
import os
for root, dirs, files in os.walk('data'):
    for f in files:
        print(os.path.join(root, f))
"
```

---

## 🔍 DIAGNOSTIC RAPIDE

### Vérifier que Flask fonctionne
```bash
curl http://localhost:5008/categories
```
**Attendu** : JSON avec liste des catégories

### Vérifier que Node.js fonctionne
```bash
curl http://localhost:3008/status
```
**Attendu** : `{"status":"ok"}`

### Vérifier les logs
```bash
# Flask affiche dans le terminal
# Chercher les erreurs

# Node.js affiche dans son terminal
# Chercher "Server running on port 3008"
```

---

## 📞 CONTACTS D'URGENCE

### Fichiers de documentation
- `INDEX_STRUCTURE_COMPLETE.md` - Structure complète
- `INDEX_CODE_FONCTIONS.md` - Toutes les fonctions
- `INDEX_API_ENDPOINTS.md` - Tous les endpoints
- `.kiro/steering/tech.md` - Stack technique
- `.kiro/steering/structure.md` - Structure détaillée

### Commandes utiles
```bash
# Lister toutes les catégories
python -c "import json; print(json.load(open('categories.json')))"

# Compter les notes
python -c "import os; print(sum(1 for r,d,f in os.walk('data') for file in f))"

# Créer backup manuel
python -c "
import shutil, datetime
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
shutil.make_archive(f'zip/backup_manuel_{timestamp}', 'zip', '.')
"
```

---

## 🎯 CHECKLIST DE RÉCUPÉRATION

- [ ] Python 3.x installé
- [ ] Node.js installé
- [ ] Dépendances Python installées (requirements.txt)
- [ ] Fichiers critiques présents (app_new.py, etc.)
- [ ] Dossier data/ intact
- [ ] categories.json valide
- [ ] category_mapping.json valide
- [ ] Port 5008 disponible
- [ ] Port 3008 disponible
- [ ] Flask démarre sans erreur
- [ ] Node.js démarre sans erreur
- [ ] Interface accessible sur http://localhost:5008
- [ ] Recherche fonctionne

---

## 🆘 DERNIER RECOURS

Si RIEN ne fonctionne :

1. **Sauvegarder le dossier data/** (VOS NOTES)
2. **Réinstaller Python et Node.js**
3. **Cloner/télécharger une version propre du projet**
4. **Restaurer le dossier data/**
5. **Réinstaller les dépendances**
6. **Redémarrer**

**Le dossier data/ contient TOUTES vos notes. Ne le supprimez JAMAIS.**
