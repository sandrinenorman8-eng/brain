# INDEX API - TOUS LES ENDPOINTS

## 🌐 SERVEUR FLASK (Port 5008)

### CATÉGORIES

#### GET /categories
**Description** : Liste toutes les catégories avec métadonnées
**Réponse** :
```json
{
  "success": true,
  "categories": {
    "todo": {"emoji": "✅", "color": "#4CAF50"},
    "memobrik": {"emoji": "🧠", "color": "#2196F3"}
  }
}
```

#### POST /add_category
**Description** : Crée une nouvelle catégorie
**Body** :
```json
{
  "name": "nouvelle_categorie",
  "emoji": "🔥",
  "color": "#FF5733",
  "parent_folder": "logiciels"
}
```
**Réponse** :
```json
{
  "success": true,
  "message": "Catégorie créée",
  "path": "logiciels/nouvelle_categorie"
}
```

#### DELETE /erase_category/<category>
**Description** : Supprime catégorie et tous ses fichiers
**Réponse** :
```json
{
  "success": true,
  "message": "Catégorie supprimée"
}
```

#### GET /open_folder/<category>
**Description** : Ouvre le dossier dans Windows Explorer
**Réponse** :
```json
{
  "success": true,
  "message": "Dossier ouvert"
}
```

---

### NOTES

#### POST /save/<category>
**Description** : Sauvegarde une note avec timestamp
**Body** :
```json
{
  "content": "Ma note importante"
}
```
**Fichier créé** : `data/{parent}/{category}/{category}_{YYYY-MM-DD}.txt`
**Format** : `HH:MM:SS: Ma note importante`
**Réponse** :
```json
{
  "success": true,
  "message": "Note sauvegardée"
}
```

#### GET /list/<category>
**Description** : Liste tous les fichiers d'une catégorie
**Réponse** :
```json
{
  "success": true,
  "files": [
    {
      "name": "todo_2025-11-16.txt",
      "date": "2025-11-16",
      "size": 1024
    }
  ]
}
```

#### GET /read/<category>/<filename>
**Description** : Lit le contenu d'un fichier
**Réponse** :
```json
{
  "success": true,
  "content": "10:30:15: Première note\n11:45:22: Deuxième note",
  "filename": "todo_2025-11-16.txt"
}
```

#### POST /upload_file
**Description** : Upload un fichier vers une catégorie
**Body** : FormData avec file et category
**Réponse** :
```json
{
  "success": true,
  "message": "Fichier uploadé",
  "filename": "document.pdf"
}
```

#### GET /all_files
**Description** : Liste TOUS les fichiers de toutes les catégories (avec cache)
**Réponse** :
```json
{
  "success": true,
  "files": [
    {
      "category": "todo",
      "filename": "todo_2025-11-16.txt",
      "path": "data/priorité/todo/todo_2025-11-16.txt",
      "size": 1024,
      "modified": "2025-11-16T10:30:00"
    }
  ]
}
```

---

### RECHERCHE

#### POST /search_content
**Description** : Recherche full-text dans toutes les notes (proxy vers Node.js)
**Body** :
```json
{
  "query": "mot clé",
  "category": "todo"
}
```
**Réponse** :
```json
{
  "success": true,
  "results": [
    {
      "file": "todo_2025-11-16.txt",
      "category": "todo",
      "matches": 3,
      "excerpts": [
        "...contexte avant mot clé contexte après..."
      ]
    }
  ]
}
```

---

### FUSION

#### POST /fusion/global
**Description** : Fusionne TOUTES les notes de toutes les catégories
**Réponse** :
```json
{
  "success": true,
  "message": "Fusion globale créée",
  "filename": "fusion_globale_2025-11-16_14-30-00.txt",
  "path": "fusion_global/fusion_globale_2025-11-16_14-30-00.txt"
}
```

#### POST /fusion/categories
**Description** : Fusionne les notes de catégories sélectionnées
**Body** :
```json
{
  "categories": ["todo", "memobrik", "scénario"]
}
```
**Réponse** :
```json
{
  "success": true,
  "message": "Fusion créée",
  "filename": "fusion_categories_todo_memobrik_scénario_2025-11-16_14-30-00.txt",
  "path": "fusion_categories/fusion_categories_todo_memobrik_scénario_2025-11-16_14-30-00.txt"
}
```

---

### WEB

#### GET /
**Description** : Sert la page principale (index.html)
**Réponse** : HTML

#### GET /all_notes
**Description** : Sert le visualiseur de notes standalone
**Réponse** : HTML

---

### UTILITAIRES

#### POST /backup_project
**Description** : Crée un backup ZIP complet du projet
**Réponse** :
```json
{
  "success": true,
  "message": "Backup créé",
  "filename": "backup_2025-11-16_14-30-00.zip",
  "path": "zip/backup_2025-11-16_14-30-00.zip",
  "size": 10485760
}
```

---

## 🟩 SERVEUR NODE.JS (Port 3008)

### POST /search
**Description** : Recherche full-text dans les fichiers
**Body** :
```json
{
  "query": "mot clé",
  "category": "todo"
}
```
**Réponse** :
```json
{
  "success": true,
  "results": [
    {
      "file": "data/priorité/todo/todo_2025-11-16.txt",
      "category": "todo",
      "matches": 3,
      "excerpts": [
        "...contexte avant mot clé contexte après..."
      ]
    }
  ],
  "total": 1,
  "query": "mot clé"
}
```

### GET /status
**Description** : Health check du serveur
**Réponse** :
```json
{
  "status": "ok",
  "service": "search-server",
  "port": 3008
}
```

---

## 🔐 CODES D'ERREUR

### 200 - Success
Opération réussie

### 400 - Bad Request
Paramètres manquants ou invalides

### 404 - Not Found
Ressource introuvable (catégorie, fichier)

### 500 - Internal Server Error
Erreur serveur (problème fichier, encodage, etc.)

### 503 - Service Unavailable
Serveur de recherche Node.js non disponible

---

## 📝 NOTES IMPORTANTES

1. **Encodage** : Tous les endpoints acceptent et retournent UTF-8
2. **CORS** : Activé sur tous les endpoints Flask
3. **Cache** : `/all_files` utilise un cache LRU, invalidé après modifications
4. **Timestamps** : Format ISO 8601 pour les dates
5. **Noms de fichiers** : Pattern `{category}_{YYYY-MM-DD}.txt`
6. **Recherche** : Insensible à la casse, recherche dans le contenu complet

---

## 🚀 EXEMPLES D'UTILISATION

### Sauvegarder une note
```javascript
fetch('http://localhost:5008/save/todo', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({content: 'Ma note'})
})
```

### Rechercher
```javascript
fetch('http://localhost:5008/search_content', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({query: 'mot clé', category: 'todo'})
})
```

### Créer une catégorie
```javascript
fetch('http://localhost:5008/add_category', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    name: 'nouvelle',
    emoji: '🔥',
    color: '#FF5733',
    parent_folder: 'logiciels'
  })
})
```
