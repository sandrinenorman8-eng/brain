# Alternative SIMPLE : Glitch (Aucune Installation)

## Pourquoi Glitch ?

- ✅ Aucune installation nécessaire
- ✅ Gratuit à vie
- ✅ Déploiement en 2 clics
- ✅ URL HTTPS automatique
- ✅ Éditeur en ligne

## Étapes (2 minutes)

### 1. Créer Projet Glitch

1. Va sur https://glitch.com
2. Clique "New Project" → "hello-express"
3. Nom du projet : `memobrik-backend` (ou autre)

### 2. Remplacer le Code

Dans `server.js`, remplace TOUT par :

```javascript
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors({ origin: /^chrome-extension:\/\/.*/ }));
app.use(express.json());

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: Date.now() });
});

app.post('/api/save', (req, res) => {
  console.log('Received:', req.body);
  res.json({ success: true, data: req.body });
});

app.get('/api/list/:category', (req, res) => {
  res.json({ category: req.params.category, files: [] });
});

app.listen(3000);
```

### 3. Récupérer l'URL

En haut à droite : "Share" → Copier l'URL
Format : `https://memobrik-backend.glitch.me`

### 4. Mettre à Jour Extension

Ouvre `G:\memobrik\extchrome\manifest.json`

Remplace :
```json
"http://localhost:5008/*"
```

Par :
```json
"https://memobrik-backend.glitch.me/*"
```

### 5. Recharger Extension

Chrome → Extensions → Recharger "Deuxième Cerveau"

## C'EST FINI !

Pas de gcloud, pas d'installation, pas de facturation.

---

## Si tu veux quand même GAE

Attends que l'installateur Google Cloud SDK finisse, puis :

1. Suis les étapes d'installation
2. Lance `gcloud init`
3. Connecte-toi avec ton compte Google
4. Lance `DEPLOY_TOUT.bat`

Mais Glitch est 100x plus simple pour usage perso.
