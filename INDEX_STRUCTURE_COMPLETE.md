# INDEX COMPLET - STRUCTURE DU PROJET DEUXIÈME CERVEAU

## 📁 ARBORESCENCE COMPLÈTE

```
memobrik/
│
├── deuxieme_cerveau/              # APPLICATION PRINCIPALE
│   ├── app_new.py                 # Point d'entrée Flask
│   ├── index.html                 # Interface utilisateur principale
│   ├── all_notes_standalone.html  # Visualiseur de notes standalone
│   ├── search-server-fixed.js     # Serveur de recherche Node.js (port 3008)
│   ├── category_path_resolver.py  # Résolution des chemins hiérarchiques
│   │
│   ├── blueprints/                # ROUTES FLASK (architecture modulaire)
│   │   ├── __init__.py
│   │   ├── category_routes.py     # Routes catégories (/categories, /add_category, /erase_category)
│   │   ├── notes_routes.py        # Routes notes (/save, /list, /read, /upload_file)
│   │   ├── search_routes.py       # Routes recherche (/search_content)
│   │   ├── web_routes.py          # Routes web (/, /all_notes)
│   │   ├── utility_routes.py      # Routes utilitaires (/open_folder, /backup_project)
│   │   └── fusion_routes.py       # Routes fusion (/fusion/global, /fusion/categories)
│   │
│   ├── services/                  # LOGIQUE MÉTIER
│   │   ├── __init__.py
│   │   ├── category_service.py    # Gestion des catégories
│   │   ├── notes_service.py       # Gestion des notes
│   │   ├── search_service.py      # Communication avec serveur Node.js
│   │   └── fusion_service.py      # Fusion de notes
│   │
│   ├── utils/                     # UTILITAIRES
│   │   ├── __init__.py
│   │   ├── file_utils.py          # Opérations fichiers (lecture/écriture UTF-8)
│   │   ├── http_utils.py          # Requêtes HTTP
│   │   └── response_utils.py      # Formatage réponses JSON
│   │
│   ├── config/                    # CONFIGURATION
│   │   ├── __init__.py
│   │   └── config.py              # Config Flask (port 5008, debug, etc.)
│   │
│   ├── static/                    # FRONTEND JAVASCRIPT
│   │   ├── script.js              # Script principal (legacy)
│   │   ├── api.js                 # Appels API
│   │   ├── ui.js                  # Gestion UI
│   │   ├── state.js               # État application
│   │   └── alphabet.js            # Navigation alphabétique
│   │
│   ├── sections/                  # COMPOSANTS HTML MODULAIRES
│   │   ├── 01_document_head.html  # <head> avec styles
│   │   ├── 02_main_content.html   # Contenu principal
│   │   ├── 03_notes_section.html  # Section notes
│   │   ├── 04_folders_section.html # Section dossiers
│   │   └── 05_javascript.html     # Scripts JS
│   │
│   ├── data/                      # DONNÉES UTILISATEUR (hiérarchique)
│   │   ├── buziness/
│   │   │   ├── association/
│   │   │   ├── idée business/
│   │   │   ├── la villa de la paix/
│   │   │   ├── lagence/
│   │   │   ├── money brick/
│   │   │   └── opportunité/
│   │   ├── cinema/
│   │   │   └── scénario/
│   │   ├── livres/
│   │   │   ├── idee philo/
│   │   │   ├── motivation/
│   │   │   ├── psychologie succès/
│   │   │   └── société de livres/
│   │   ├── logiciels/
│   │   │   ├── agenda intelligent/
│   │   │   ├── brikmagik/
│   │   │   ├── chrono brique/
│   │   │   ├── kodi brik/
│   │   │   ├── memobrik/
│   │   │   ├── promptbrik/
│   │   │   └── scrap them all/
│   │   ├── priorité/
│   │   │   └── todo/
│   │   └── series/
│   │       ├── GEN Z/
│   │       └── projet youtube/
│   │
│   ├── fusion_categories/         # Résultats fusion par catégorie
│   ├── fusion_global/             # Résultats fusion globale
│   ├── backups/                   # Backups automatiques
│   ├── archives/                  # Anciennes versions
│   ├── tests/                     # Tests unitaires
│   │   ├── test_integration.py
│   │   ├── test_file_utils.py
│   │   └── conftest.py
│   │
│   ├── automation/                # Automatisation Chrome
│   │   ├── chrome_extension/
│   │   ├── server_host.py
│   │   └── install_native_messaging.bat
│   │
│   ├── docs/                      # Documentation
│   │
│   ├── categories.json            # Définition catégories (emoji, couleur)
│   ├── category_mapping.json      # Mapping hiérarchique des chemins
│   ├── requirements.txt           # Dépendances Python
│   ├── package.json               # Métadonnées Node.js
│   ├── config.ini                 # Configuration alternative
│   │
│   ├── START.bat                  # Démarrage complet (Flask + Node.js)
│   ├── STOP.bat                   # Arrêt des services
│   ├── INSTALL.bat                # Installation dépendances
│   └── RUN_TESTS.bat              # Lancement tests
│
├── backend/                       # Autre backend (si utilisé)
├── extchrome/                     # Extension Chrome
├── docs_chrome_extension/         # Documentation extension
├── zip/                           # Archives backups manuels
│
├── .kiro/                         # Configuration Kiro AI
│   └── steering/                  # Règles de guidage
│       ├── tech.md                # Stack technique
│       ├── structure.md           # Structure projet
│       └── product.md             # Vue produit
│
└── .vscode/                       # Configuration VS Code
    └── settings.json
```

## 📊 STATISTIQUES

- **Lignes de code Python** : ~3000+
- **Lignes de code JavaScript** : ~2000+
- **Nombre de routes Flask** : 20+
- **Nombre de catégories** : 25+
- **Ports utilisés** : 5008 (Flask), 3008 (Node.js)

## 🔑 FICHIERS CRITIQUES (NE JAMAIS SUPPRIMER)

1. `deuxieme_cerveau/app_new.py` - Application principale
2. `deuxieme_cerveau/category_mapping.json` - Mapping des chemins
3. `deuxieme_cerveau/categories.json` - Définition catégories
4. `deuxieme_cerveau/data/` - Toutes les notes utilisateur
5. `deuxieme_cerveau/category_path_resolver.py` - Résolution chemins

## 📦 DÉPENDANCES

### Python
- Flask 3.0.0
- requests 2.32.3
- python-dotenv 1.0.0

### Node.js
- Modules natifs uniquement (fs, http, path)

## 🚀 DÉMARRAGE RAPIDE

```bash
cd deuxieme_cerveau
START.bat
```

Accès : http://localhost:5008
