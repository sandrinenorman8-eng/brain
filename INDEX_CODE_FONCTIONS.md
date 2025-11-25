# INDEX CODE - FONCTIONS ET RESPONSABILITÉS

## 🐍 PYTHON - BACKEND FLASK

### app_new.py
**Rôle** : Point d'entrée de l'application Flask

**Fonctions principales** :
- `create_app()` : Crée et configure l'application Flask
  - Enregistre tous les blueprints
  - Configure CORS
  - Définit les error handlers (404, 500)
- `if __name__ == '__main__'` : Lance le serveur sur port 5008

**Dépendances** : Tous les blueprints, Config

---

### category_path_resolver.py
**Rôle** : Résolution des chemins de catégories avec hiérarchie

**Fonctions** :
- `load_category_mapping()` : Charge category_mapping.json
- `get_category_path(category_name)` : Retourne chemin relatif (ex: "buziness/association")
- `get_absolute_category_path(category_name)` : Retourne chemin absolu complet
- `get_all_categories()` : Liste toutes les catégories disponibles

**Fichier critique** : category_mapping.json

---

## 📘 BLUEPRINTS (Routes Flask)

### blueprints/category_routes.py
**Routes** :
- `GET /categories` : Liste toutes les catégories avec emoji/couleur
- `POST /add_category` : Crée nouvelle catégorie
  - Paramètres : name, emoji, color, parent_folder
  - Crée dossier physique
  - Met à jour categories.json et category_mapping.json
- `DELETE /erase_category/<category>` : Supprime catégorie et fichiers
- `GET /open_folder/<category>` : Ouvre dossier dans Windows Explorer

**Fonctions internes** :
- Validation des noms de catégories
- Gestion de la hiérarchie parent/enfant

---

### blueprints/notes_routes.py
**Routes** :
- `POST /save/<category>` : Sauvegarde note avec timestamp
  - Format : `HH:MM:SS: contenu`
  - Fichier : `{category}_{YYYY-MM-DD}.txt`
- `GET /list/<category>` : Liste fichiers d'une catégorie
  - Tri par date décroissante
- `GET /read/<category>/<filename>` : Lit contenu d'un fichier
  - Gère encodage UTF-8, cp1252, latin-1
- `POST /upload_file` : Upload fichier vers catégorie
- `GET /all_files` : Liste tous fichiers (avec cache)
  - Cache invalidé après modifications

**Fonctions internes** :
- `_get_all_files_cached()` : Cache LRU pour performance
- Gestion multi-encodage pour compatibilité

---

### blueprints/search_routes.py
**Routes** :
- `POST /search_content` : Proxy vers serveur Node.js
  - Paramètres : query, category (optionnel)
  - Retourne résultats avec extraits contextuels

**Communication** : HTTP vers localhost:3008

---

### blueprints/fusion_routes.py
**Routes** :
- `POST /fusion/global` : Fusionne toutes les notes
  - Crée fichier dans fusion_global/
  - Format : fusion_globale_{timestamp}.txt
- `POST /fusion/categories` : Fusionne catégories sélectionnées
  - Paramètres : categories (array)
  - Crée fichier dans fusion_categories/

**Fonctions internes** :
- Tri chronologique des entrées
- Préservation des timestamps originaux

---

### blueprints/web_routes.py
**Routes** :
- `GET /` : Sert index.html
- `GET /all_notes` : Sert all_notes_standalone.html

---

### blueprints/utility_routes.py
**Routes** :
- `POST /backup_project` : Crée backup ZIP complet
  - Destination : zip/backup_{timestamp}.zip
  - Exclut : .venv, __pycache__, node_modules

---

## 🛠️ SERVICES (Logique Métier)

### services/category_service.py
**Fonctions** :
- `get_categories()` : Charge categories.json
- `create_category(name, emoji, color, parent)` : Crée catégorie
- `delete_category(name)` : Supprime catégorie
- `update_category_mapping(name, path)` : Met à jour mapping

---

### services/notes_service.py
**Fonctions** :
- `save_note(category, content)` : Sauvegarde note
- `list_notes(category)` : Liste notes d'une catégorie
- `read_note(category, filename)` : Lit note
- `get_all_notes()` : Récupère toutes les notes (cache)

---

### services/search_service.py
**Fonctions** :
- `search_in_node(query, category=None)` : Appelle serveur Node.js
- `is_search_server_running()` : Vérifie disponibilité serveur

---

### services/fusion_service.py
**Fonctions** :
- `merge_all_notes()` : Fusionne toutes les notes
- `merge_categories(category_list)` : Fusionne catégories sélectionnées
- `parse_note_entries(content)` : Parse entrées avec timestamps
- `sort_entries_chronologically(entries)` : Tri chronologique

---

## 🔧 UTILS (Utilitaires)

### utils/file_utils.py
**Fonctions** :
- `read_file_with_encoding(filepath)` : Lecture multi-encodage
  - Essaie : UTF-8 → cp1252 → latin-1 → iso-8859-1
- `write_file_utf8(filepath, content)` : Écriture UTF-8
- `ensure_directory_exists(path)` : Crée dossier si nécessaire
- `get_file_list(directory)` : Liste fichiers avec métadonnées

---

### utils/http_utils.py
**Fonctions** :
- `make_request(url, method, data=None)` : Requête HTTP générique
- `check_server_health(url)` : Vérifie santé serveur

---

### utils/response_utils.py
**Fonctions** :
- `success_response(data, message=None)` : Réponse succès JSON
- `error_response(error, status_code=400)` : Réponse erreur JSON
- `format_file_metadata(file_info)` : Formate métadonnées fichier

---

## 🟨 JAVASCRIPT - FRONTEND

### static/script.js (Legacy - monolithique)
**Fonctions principales** :
- `saveNote()` : Sauvegarde note via API
- `loadCategories()` : Charge et affiche catégories
- `loadFiles(category)` : Charge fichiers d'une catégorie
- `readFile(category, filename)` : Lit et affiche fichier
- `searchContent()` : Recherche full-text
- `openFolder(category)` : Ouvre dossier système
- `deleteCategory(category)` : Supprime catégorie
- `uploadFile()` : Upload fichier
- `fusionGlobal()` : Fusion globale
- `fusionCategories()` : Fusion catégories sélectionnées

---

### static/api.js (Modulaire)
**Fonctions** :
- `API.saveNote(category, content)` : POST /save
- `API.getCategories()` : GET /categories
- `API.listFiles(category)` : GET /list
- `API.readFile(category, filename)` : GET /read
- `API.search(query, category)` : POST /search_content
- `API.uploadFile(category, file)` : POST /upload_file
- `API.fusionGlobal()` : POST /fusion/global
- `API.fusionCategories(categories)` : POST /fusion/categories

---

### static/ui.js (Modulaire)
**Fonctions** :
- `UI.showNotification(message, type)` : Affiche notification
- `UI.renderCategories(categories)` : Affiche liste catégories
- `UI.renderFiles(files)` : Affiche liste fichiers
- `UI.renderFileContent(content)` : Affiche contenu fichier
- `UI.updateAlphabetFilter()` : Met à jour filtre alphabétique

---

### static/state.js (Modulaire)
**Variables d'état** :
- `State.currentCategory` : Catégorie sélectionnée
- `State.currentFile` : Fichier ouvert
- `State.categories` : Liste catégories
- `State.files` : Liste fichiers

---

### static/alphabet.js (Modulaire)
**Fonctions** :
- `Alphabet.filter(letter)` : Filtre catégories par lettre
- `Alphabet.reset()` : Réinitialise filtre

---

## 🟩 NODE.JS - SERVEUR DE RECHERCHE

### search-server-fixed.js
**Rôle** : Serveur de recherche full-text indépendant (port 3008)

**Routes** :
- `POST /search` : Recherche dans fichiers
  - Paramètres : query, category (optionnel)
  - Retourne : fichiers + extraits contextuels
- `GET /status` : Health check

**Fonctions** :
- `searchInFiles(query, category)` : Recherche récursive
- `extractContext(content, query)` : Extrait contexte autour du match
- `readFileWithEncoding(filepath)` : Lecture multi-encodage

**Algorithme** :
1. Parcours récursif du dossier data/
2. Lecture de chaque fichier .txt
3. Recherche insensible à la casse
4. Extraction de 100 caractères de contexte
5. Retour JSON avec métadonnées

---

## 📋 FICHIERS DE CONFIGURATION

### categories.json
**Structure** :
```json
{
  "category_name": {
    "emoji": "🔥",
    "color": "#FF5733"
  }
}
```

### category_mapping.json
**Structure** :
```json
{
  "category_name": "parent_folder/category_name"
}
```

### config/config.py
**Variables** :
- `PORT = 5008`
- `HOST = '0.0.0.0'`
- `FLASK_DEBUG = False`
- `DATA_DIR = 'data'`
- `SEARCH_SERVER_URL = 'http://localhost:3008'`

---

## 🔄 FLUX DE DONNÉES

### Sauvegarde de note :
1. Frontend : `API.saveNote()` → POST /save/{category}
2. Backend : `notes_routes.py` → `notes_service.save_note()`
3. Service : `file_utils.write_file_utf8()`
4. Fichier : `data/{parent}/{category}/{category}_{date}.txt`
5. Cache : Invalidation de `_get_all_files_cached()`

### Recherche :
1. Frontend : `API.search()` → POST /search_content
2. Backend : `search_routes.py` → `search_service.search_in_node()`
3. Node.js : `search-server-fixed.js` → `searchInFiles()`
4. Retour : JSON avec résultats + contexte

### Fusion globale :
1. Frontend : `API.fusionGlobal()` → POST /fusion/global
2. Backend : `fusion_routes.py` → `fusion_service.merge_all_notes()`
3. Service : Lecture de tous les fichiers + tri chronologique
4. Fichier : `fusion_global/fusion_globale_{timestamp}.txt`

---

## 🎯 POINTS D'ENTRÉE CRITIQUES

1. **Démarrage application** : `app_new.py` ligne ~45
2. **Résolution chemins** : `category_path_resolver.py` ligne ~15
3. **Sauvegarde notes** : `services/notes_service.py` ligne ~20
4. **Recherche** : `search-server-fixed.js` ligne ~30
5. **Fusion** : `services/fusion_service.py` ligne ~10

---

## ⚠️ FONCTIONS AVEC CACHE

- `notes_service.get_all_notes()` : Cache LRU
- **Invalidation** : Après save, upload, delete
- **Commande** : `_get_all_files_cached.cache_clear()`
