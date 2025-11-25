# 3. PHASE 1 : DÉPLOIEMENT DU BACKEND {#3-phase1}

## 3.1 Choix de la Stratégie de Déploiement

**Option Unique : Google App Engine (PRODUCTION)**

Google App Engine offre :
- ✅ Scaling automatique
- ✅ HTTPS natif
- ✅ Intégration GCP (Cloud SQL, Firestore, etc.)
- ✅ Environnement Standard ou Flexible
- ✅ Monitoring et logging intégrés

## 3.2 Préparation du Projet Google Cloud

### Étape 1.1 : Créer le Projet GCP

1. Aller sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créer un nouveau projet ou sélectionner un existant
3. Activer la facturation pour le projet
4. Noter le `PROJECT_ID`

### Étape 1.2 : Initialiser App Engine

```bash
# Installer Google Cloud SDK
# Windows: https://cloud.google.com/sdk/docs/install
# Linux/Mac: curl https://sdk.cloud.google.com | bash

# Se connecter
gcloud auth login

# Sélectionner le projet
gcloud config set project YOUR_PROJECT_ID

# Créer l'application App Engine (choisir région)
gcloud app create --region=europe-west1
```

**⚠️ IMPORTANT** : La région ne peut pas être modifiée après création !

Régions recommandées :
- `europe-west1` (Belgique)
- `europe-west3` (Francfort)
- `us-central1` (Iowa)

## 3.3 Développement du Backend

### Structure du Projet

```
backend/
├── app.yaml          # Configuration App Engine
├── src/
│   └── index.js      # Code serveur
├── package.json
└── .gcloudignore     # Fichiers à ignorer
```

### Fichier app.yaml

```yaml
runtime: nodejs20

instance_class: F1

env_variables:
  NODE_ENV: "production"
  JWT_SECRET: "your-secret-here"

automatic_scaling:
  min_instances: 0
  max_instances: 10
  target_cpu_utilization: 0.65

handlers:
- url: /api/.*
  script: auto
  secure: always

- url: /.*
  script: auto
  secure: always
```

### Code Backend (src/index.js)

```javascript
const express = require('express');
const cors = require('cors');
const app = express();

// Configuration CORS pour Extension Chrome
const corsOptions = {
  origin: [
    'chrome-extension://*',
    /^chrome-extension:\/\/[a-z]{32}$/
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  exposedHeaders: ['X-Total-Count'],
  maxAge: 86400
};

app.use(cors(corsOptions));
app.use(express.json());

// Empêcher cache CDN des préflights
app.options('*', (req, res) => {
  res.set('Cache-Control', 'no-store');
  res.sendStatus(204);
});

// Route de santé
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: Date.now(),
    service: 'backend-gae'
  });
});

// Démarrer serveur
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Fichier .gcloudignore

```
node_modules/
.git/
.env
*.log
test/
.vscode/
```

## 3.4 Déploiement sur App Engine

### Commande de Déploiement

```bash
# Depuis le dossier backend/
gcloud app deploy

# Ou spécifier le fichier
gcloud app deploy app.yaml

# Déployer avec version spécifique
gcloud app deploy --version=v1
```

### Récupérer l'URL Déployée

```bash
# Obtenir l'URL
gcloud app browse

# Ou construire manuellement
# Format: https://PROJECT_ID.REGION_ID.r.appspot.com
# Exemple: https://my-backend-123456.ew.r.appspot.com
```

## 3.5 Configuration des Variables d'Environnement

### Méthode 1 : Dans app.yaml

```yaml
env_variables:
  JWT_SECRET: "your-secret-here"
  DATABASE_URL: "postgresql://..."
```

### Méthode 2 : Secret Manager (Recommandé)

```bash
# Créer un secret
echo -n "your-secret-value" | gcloud secrets create jwt-secret --data-file=-

# Donner accès à App Engine
gcloud secrets add-iam-policy-binding jwt-secret \
  --member="serviceAccount:YOUR_PROJECT_ID@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

Dans app.yaml :
```yaml
env_variables:
  JWT_SECRET: ${JWT_SECRET}
```

## 3.6 Validation de l'Accessibilité

### Test avec curl

```bash
# Vérifier HTTPS et headers
curl -I https://YOUR_PROJECT_ID.REGION.r.appspot.com/api/health

# Test complet
curl https://YOUR_PROJECT_ID.REGION.r.appspot.com/api/health
```

### Réponse Attendue

```
HTTP/2 200
access-control-allow-origin: chrome-extension://*
content-type: application/json
cache-control: no-store

{"status":"ok","timestamp":1234567890,"service":"backend-gae"}
```

## 3.7 Monitoring et Logs

```bash
# Voir les logs en temps réel
gcloud app logs tail -s default

# Voir les logs dans la console
# https://console.cloud.google.com/logs
```
