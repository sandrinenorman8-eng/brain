# 🎯 INDEX MASTER - DEUXIÈME CERVEAU

## 📚 DOCUMENTATION COMPLÈTE DE RÉCUPÉRATION

Ce document est le point d'entrée principal pour comprendre et récupérer le projet **Deuxième Cerveau** en cas de catastrophe.

---

## 🗂️ LISTE DES INDEX DISPONIBLES

### 1. **INDEX_STRUCTURE_COMPLETE.md**
📁 **Arborescence complète du projet**
- Structure des dossiers
- Organisation des fichiers
- Hiérarchie des modules
- Statistiques du projet

**Utiliser quand** : Vous devez comprendre où se trouve chaque fichier

---

### 2. **INDEX_CODE_FONCTIONS.md**
⚙️ **Toutes les fonctions et leur rôle**
- Fonctions Python (Flask, services, utils)
- Fonctions JavaScript (frontend)
- Fonctions Node.js (serveur recherche)
- Flux de données
- Points d'entrée critiques

**Utiliser quand** : Vous devez modifier ou débugger du code

---

### 3. **INDEX_API_ENDPOINTS.md**
🌐 **Tous les endpoints API**
- Routes Flask (port 5008)
- Routes Node.js (port 3008)
- Paramètres et réponses
- Codes d'erreur
- Exemples d'utilisation

**Utiliser quand** : Vous devez intégrer ou tester l'API

---

### 4. **INDEX_FICHIERS_DONNEES.md**
💾 **Structure des données utilisateur**
- Hiérarchie du dossier data/
- Mapping catégories → chemins
- Format des fichiers de notes
- Métadonnées des catégories
- Backups et fusions

**Utiliser quand** : Vous devez récupérer ou migrer des données

---

### 5. **INDEX_DEMARRAGE_URGENCE.md**
🚨 **Guide de récupération d'urgence**
- Vérification des fichiers critiques
- Réinstallation des dépendances
- Démarrage manuel
- Problèmes courants et solutions
- Checklist de récupération

**Utiliser quand** : L'application ne démarre plus

---

### 6. **NAVIGATION.md**
🧭 **Navigation rapide (workaround Kiro)**
- Liste des fichiers principaux
- Chemins à copier/coller dans Ctrl+P
- Organisation par catégorie

**Utiliser quand** : L'explorateur de fichiers ne fonctionne pas

---

## 🎯 SCÉNARIOS D'UTILISATION

### Scénario 1 : "Je reprends le projet après 6 mois"
1. Lire **INDEX_MASTER.md** (ce fichier)
2. Lire **INDEX_STRUCTURE_COMPLETE.md** pour comprendre l'organisation
3. Lire **INDEX_DEMARRAGE_URGENCE.md** pour démarrer l'application
4. Consulter **INDEX_API_ENDPOINTS.md** pour les fonctionnalités

### Scénario 2 : "L'application ne démarre plus"
1. Ouvrir **INDEX_DEMARRAGE_URGENCE.md**
2. Suivre la checklist de récupération
3. Vérifier les fichiers critiques
4. Réinstaller les dépendances

### Scénario 3 : "Je dois modifier une fonctionnalité"
1. Consulter **INDEX_CODE_FONCTIONS.md** pour trouver la fonction
2. Consulter **INDEX_STRUCTURE_COMPLETE.md** pour localiser le fichier
3. Consulter **INDEX_API_ENDPOINTS.md** si c'est une route API

### Scénario 4 : "J'ai perdu des données"
1. Ouvrir **INDEX_FICHIERS_DONNEES.md**
2. Vérifier les backups dans zip/
3. Vérifier les fusions dans fusion_global/
4. Suivre la procédure de récupération

### Scénario 5 : "Je dois intégrer avec une autre application"
1. Consulter **INDEX_API_ENDPOINTS.md**
2. Tester les endpoints avec curl ou Postman
3. Consulter **INDEX_CODE_FONCTIONS.md** pour la logique métier

---

## 🔑 INFORMATIONS CRITIQUES

### Ports utilisés
- **5008** : Serveur Flask (application principale)
- **3008** : Serveur Node.js (recherche full-text)

### Fichiers à NE JAMAIS supprimer
1. `deuxieme_cerveau/data/` - TOUTES VOS NOTES
2. `deuxieme_cerveau/categories.json` - Définition des catégories
3. `deuxieme_cerveau/category_mapping.json` - Mapping hiérarchique
4. `deuxieme_cerveau/app_new.py` - Application principale
5. `deuxieme_cerveau/category_path_resolver.py` - Résolution chemins

### Dépendances requises
**Python** :
- Flask 3.0.0
- requests 2.32.3
- python-dotenv 1.0.0

**Node.js** :
- Version 18.x ou 20.x
- Modules natifs uniquement (fs, http, path)

### Commandes de démarrage rapide
```bash
cd deuxieme_cerveau
START.bat
```

Ou manuellement :
```bash
# Terminal 1
python app_new.py

# Terminal 2
node search-server-fixed.js
```

### URLs d'accès
- Interface principale : http://localhost:5008
- Visualiseur de notes : http://localhost:5008/all_notes
- API catégories : http://localhost:5008/categories
- Health check recherche : http://localhost:3008/status

---

## 📊 ARCHITECTURE SIMPLIFIÉE

```
┌─────────────────────────────────────────────────────────┐
│                    NAVIGATEUR                           │
│              http://localhost:5008                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              SERVEUR FLASK (5008)                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Blueprints (Routes)                             │   │
│  │  - category_routes.py                            │   │
│  │  - notes_routes.py                               │   │
│  │  - search_routes.py ──────────┐                  │   │
│  │  - fusion_routes.py           │                  │   │
│  │  - web_routes.py              │                  │   │
│  │  - utility_routes.py          │                  │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Services (Logique métier)                       │   │
│  │  - category_service.py                           │   │
│  │  - notes_service.py                              │   │
│  │  - search_service.py                             │   │
│  │  - fusion_service.py                             │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Utils (Utilitaires)                             │   │
│  │  - file_utils.py (lecture/écriture UTF-8)        │   │
│  │  - http_utils.py                                 │   │
│  │  - response_utils.py                             │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         SERVEUR NODE.JS (3008)                          │
│         search-server-fixed.js                          │
│         - Recherche full-text                           │
│         - Extraction de contexte                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              SYSTÈME DE FICHIERS                        │
│                                                         │
│  data/                  (Notes utilisateur)             │
│  categories.json        (Définition catégories)         │
│  category_mapping.json  (Mapping hiérarchique)          │
│  fusion_global/         (Fusions globales)              │
│  fusion_categories/     (Fusions par catégorie)         │
│  zip/                   (Backups)                       │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 DÉMARRAGE EN 3 ÉTAPES

### 1. Vérifier les prérequis
```bash
python --version    # Doit être 3.x
node --version      # Doit être 18.x ou 20.x
```

### 2. Installer les dépendances
```bash
cd deuxieme_cerveau
pip install -r requirements.txt
```

### 3. Démarrer l'application
```bash
START.bat
```

---

## 📞 AIDE RAPIDE

### Problème : L'explorateur de fichiers Kiro est vide
**Solution** : Utiliser Ctrl+P pour ouvrir les fichiers
**Référence** : NAVIGATION.md

### Problème : L'application ne démarre pas
**Solution** : Suivre INDEX_DEMARRAGE_URGENCE.md

### Problème : Je ne trouve pas une fonction
**Solution** : Chercher dans INDEX_CODE_FONCTIONS.md

### Problème : Je ne comprends pas l'API
**Solution** : Consulter INDEX_API_ENDPOINTS.md

### Problème : J'ai perdu des données
**Solution** : Consulter INDEX_FICHIERS_DONNEES.md section "Backups"

---

## 🎓 POUR ALLER PLUS LOIN

### Documentation technique détaillée
- `.kiro/steering/tech.md` - Stack technique complète
- `.kiro/steering/structure.md` - Structure détaillée
- `.kiro/steering/product.md` - Vue produit

### Tests
```bash
cd deuxieme_cerveau
RUN_TESTS.bat
```

### Backup manuel
```bash
cd deuxieme_cerveau
python -c "import shutil, datetime; shutil.make_archive(f'../zip/backup_{datetime.datetime.now().strftime(\"%Y%m%d_%H%M%S\")}', 'zip', '.')"
```

---

## ✅ CHECKLIST DE SANTÉ DU PROJET

- [ ] Python 3.x installé
- [ ] Node.js installé
- [ ] Dépendances Python installées
- [ ] Fichier app_new.py présent
- [ ] Fichier search-server-fixed.js présent
- [ ] Dossier data/ intact
- [ ] categories.json valide
- [ ] category_mapping.json valide
- [ ] Flask démarre sur port 5008
- [ ] Node.js démarre sur port 3008
- [ ] Interface accessible
- [ ] Recherche fonctionne
- [ ] Sauvegarde de notes fonctionne

---

## 🆘 CONTACT D'URGENCE

En cas de problème critique :
1. Sauvegarder le dossier `data/` (VOS NOTES)
2. Consulter INDEX_DEMARRAGE_URGENCE.md
3. Vérifier les backups dans `zip/`
4. Reconstruire depuis les index

**Le dossier data/ contient TOUTES vos notes. C'est le seul fichier vraiment irremplaçable.**

---

*Dernière mise à jour : 2025-11-16*
*Version : 1.0*


---

## 🧠 SYSTÈME DE FUSION INTELLIGENTE (IA)

### Nouveau : Organisation Automatique par IA

Le système de Fusion Intelligente a été restauré ! Il transforme vos notes brutes en contenu structuré.

**Accès** : Bouton "🧠 Fusion IA" dans l'interface principale

**Fonctionnalités** :
- Organisation automatique en chapitres
- Création de bullet points
- Structuration hiérarchique
- Résumé des points clés

**Documentation complète** : `deuxieme_cerveau/docs/FUSION_INTELLIGENTE.md`

**Fichiers critiques** :
- `fusion_intelligente.html` - Interface utilisateur
- `blueprints/ai_routes.py` - Routes API
- `services/ai_service.py` - Logique IA
- `config.ini` - Configuration (clé API Groq)

**Endpoints** :
- `GET /fusion_intelligente` - Page d'interface
- `POST /ai/organize` - Organise une fusion
- `GET /ai/test` - Teste la connexion IA
- `GET /ai/list_fusions` - Liste les fusions disponibles

**Résultats** : Sauvegardés dans `fusion_organized/`

**API utilisée** : Groq (llama-3.1-70b-versatile) - Gratuit
