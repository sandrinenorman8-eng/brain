# Guide Complet : Déploiement Backend sur Google App Engine

## Vue d'ensemble

Ce guide couvre toutes les étapes pour déployer un backend sur Google App Engine (GAE) pour une extension Chrome.

---

## 1. Préparation du Projet Google Cloud

### 1.1 Créer le Projet

- [ ] Aller sur [Google Cloud Console](https://console.cloud.google.com/)
- [ ] Créer un nouveau projet ou sélectionner un existant
- [ ] Noter le `PROJECT_ID`
- [ ] Activer la facturation

### 1.2 Activer les APIs Nécessaires

```bash
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### 1.3 Initialiser App Engine

```bash
# Choisir une région (ne peut pas être modifiée après)
gcloud app create --region=europe-west1
```

**Régions recommandées :**
- `europe-west1` (Belgique)
- `europe-west3` (Francfort)
- `us-central1` (Iowa)

### 1.4 Installer Google Cloud SDK

```bash
# Windows: Télécharger depuis
# https://cloud.google.com/sdk/docs/install

# Linux/Mac
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Vérifier installation
gcloud version
```

### 1.5 Configurer IAM et Permissions

- [ ] Vérifier rôles : `roles/appengine.appAdmin`, `roles/cloudbuild.builds.editor`
- [ ] Configurer compte de service si nécessaire

---

## 2. Développement du Backend

### 2.1 Structure du Projet

```
backend/
├── app.yaml              # Configuration App Engine
├── src/
│   └── index.js          # Code serveur
├── package.json          # Dépendances Node.js
├── .gcloudignore         # Fichiers à ignorer
└── README.md
```

### 2.2 Créer app.yaml

```yaml
runtime: nodejs20

instance_class: F1

env_variables:
  NODE_ENV: "production"

automatic_scaling:
  min_instances: 0
  max_instances: 10
  target_cpu_utilization: 0.65

handlers:
- url: /api/.*
  script: auto
  secure: always
```

### 2.3 Code Backend Compatible GAE

**Points clés :**
- [ ] Serveur écoute sur `process.env.PORT || 8080`
- [ ] Application stateless (pas de sessions locales)
- [ ] CORS configuré pour extensions Chrome
- [ ] Gestion des préflights OPTIONS

```javascript
const express = require('express');
const cors = require('cors');
const app = express();

const corsOptions = {
  origin: [
    'chrome-extension://*',
    /^chrome-extension:\/\/[a-z]{32}$/
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
};

app.use(cors(corsOptions));

app.options('*', (req, res) => {
  res.set('Cache-Control', 'no-store');
  res.sendStatus(204);
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: Date.now() });
});

const PORT = process.env.PORT || 8080;
app.listen(PORT);
```

### 2.4 Créer .gcloudignore

```
node_modules/
.git/
.env
*.log
test/
.vscode/
```

---

## 3. Configuration de l'Architecture

### 3.1 Environnement Standard vs Flexible

**Standard (Recommandé pour API simples) :**
- ✅ Démarrage rapide
- ✅ Scaling à zéro
- ✅ Moins cher
- ❌ Limitations runtime

**Flexible (Pour besoins avancés) :**
- ✅ Plus de contrôle
- ✅ Docker custom
- ❌ Plus cher
- ❌ Pas de scaling à zéro

### 3.2 Intégration Services GCP

**Cloud SQL :**
```yaml
# Dans app.yaml
beta_settings:
  cloud_sql_instances: PROJECT_ID:REGION:INSTANCE_NAME
```

**Firestore :**
```bash
gcloud services enable firestore.googleapis.com
```

**Cloud Storage :**
```bash
gcloud services enable storage-api.googleapis.com
```

### 3.3 Configuration Multi-Services

Si plusieurs backends :

```
project/
├── backend-api/
│   └── app.yaml (service: api)
├── backend-admin/
│   └── app.yaml (service: admin)
└── dispatch.yaml
```

**dispatch.yaml :**
```yaml
dispatch:
- url: "*/api/*"
  service: api
- url: "*/admin/*"
  service: admin
```

### 3.4 Tâches Planifiées (Cron)

**cron.yaml :**
```yaml
cron:
- description: "Cleanup old data"
  url: /api/cron/cleanup
  schedule: every 24 hours
```

Déployer :
```bash
gcloud app deploy cron.yaml
```

---

## 4. Déploiement

### 4.1 Première Déploiement

```bash
# Se connecter
gcloud auth login

# Sélectionner projet
gcloud config set project YOUR_PROJECT_ID

# Déployer
cd backend/
gcloud app deploy

# Ouvrir dans navigateur
gcloud app browse
```

### 4.2 Déploiement avec Version

```bash
# Déployer version spécifique
gcloud app deploy --version=v1 --no-promote

# Migrer trafic vers nouvelle version
gcloud app services set-traffic default --splits=v1=1
```

### 4.3 Variables d'Environnement

**Méthode 1 - app.yaml :**
```yaml
env_variables:
  JWT_SECRET: "secret-value"
```

**Méthode 2 - Secret Manager (Recommandé) :**
```bash
# Créer secret
echo -n "secret-value" | gcloud secrets create jwt-secret --data-file=-

# Donner accès
gcloud secrets add-iam-policy-binding jwt-secret \
  --member="serviceAccount:PROJECT_ID@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 4.4 Vérification Déploiement

```bash
# Récupérer URL
PROJECT_ID=$(gcloud config get-value project)
REGION=$(gcloud app describe --format="value(locationId)")
URL="https://${PROJECT_ID}.${REGION}.r.appspot.com"

# Tester
curl $URL/api/health
```

---

## 5. Production, Monitoring et Scalabilité

### 5.1 Gestion du Trafic

```bash
# Lister versions
gcloud app versions list

# Split traffic (A/B testing)
gcloud app services set-traffic default --splits=v1=0.5,v2=0.5

# Migrer 100% vers v2
gcloud app services set-traffic default --splits=v2=1
```

### 5.2 Configuration Scaling

**Dans app.yaml :**
```yaml
automatic_scaling:
  min_instances: 1          # Toujours 1 instance active
  max_instances: 20         # Max 20 instances
  target_cpu_utilization: 0.65
  target_throughput_utilization: 0.75
```

### 5.3 Monitoring et Logs

```bash
# Logs en temps réel
gcloud app logs tail -s default

# Logs dans console
# https://console.cloud.google.com/logs

# Métriques
# https://console.cloud.google.com/monitoring
```

### 5.4 Alertes

Dans Cloud Console :
1. Monitoring → Alerting
2. Créer politique d'alerte
3. Conditions : CPU > 80%, Erreurs > 5%, etc.
4. Notifications : Email, SMS, Slack

### 5.5 Sécurité

- [ ] Configurer IAM correctement
- [ ] Utiliser Secret Manager pour secrets
- [ ] Activer HTTPS uniquement (`secure: always`)
- [ ] Configurer firewall si nécessaire
- [ ] Auditer accès régulièrement

### 5.6 Coûts et Quotas

```bash
# Voir utilisation
gcloud app instances list

# Configurer budget
# Console → Billing → Budgets & alerts
```

**Optimisations :**
- Utiliser `min_instances: 0` si possible
- Choisir `instance_class` adapté (F1, F2, F4)
- Nettoyer versions anciennes

---

## 6. Maintenance et Bonnes Pratiques

### 6.1 Gestion des Versions

```bash
# Supprimer version
gcloud app versions delete v1

# Lister toutes versions
gcloud app versions list --service=default
```

### 6.2 Rollback

```bash
# Revenir à version précédente
gcloud app services set-traffic default --splits=v1=1
```

### 6.3 CI/CD

**Exemple GitHub Actions :**
```yaml
name: Deploy to GAE

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - uses: google-github-actions/setup-gcloud@v0
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}
      
      - name: Deploy
        run: gcloud app deploy
```

### 6.4 Documentation

- [ ] Documenter endpoints API (OpenAPI/Swagger)
- [ ] Maintenir README à jour
- [ ] Documenter variables d'environnement
- [ ] Garder changelog des versions

### 6.5 Mises à Jour Runtime

```bash
# Vérifier runtimes disponibles
gcloud app runtimes list

# Mettre à jour dans app.yaml
runtime: nodejs20  # Nouvelle version
```

---

## 7. Checklist Finale

### Avant Production

- [ ] Tests complets de l'API
- [ ] CORS configuré correctement
- [ ] Variables d'environnement en Secret Manager
- [ ] Monitoring et alertes configurés
- [ ] Budget et quotas définis
- [ ] Documentation à jour
- [ ] Backup/rollback plan
- [ ] Sécurité auditée

### Après Déploiement

- [ ] Vérifier health endpoint
- [ ] Tester depuis extension Chrome
- [ ] Vérifier logs pour erreurs
- [ ] Monitorer métriques
- [ ] Valider coûts
- [ ] Nettoyer versions anciennes

---

## 8. Ressources

- [Documentation App Engine](https://cloud.google.com/appengine/docs)
- [Guide Node.js](https://cloud.google.com/appengine/docs/standard/nodejs)
- [Secret Manager](https://cloud.google.com/secret-manager/docs)
- [Monitoring](https://cloud.google.com/monitoring/docs)
- [Pricing Calculator](https://cloud.google.com/products/calculator)

---

## Commandes Rapides

```bash
# Setup initial
gcloud auth login
gcloud config set project PROJECT_ID
gcloud app create --region=europe-west1

# Déployer
gcloud app deploy

# Logs
gcloud app logs tail

# Ouvrir app
gcloud app browse

# Versions
gcloud app versions list
gcloud app versions delete OLD_VERSION

# Rollback
gcloud app services set-traffic default --splits=OLD_VERSION=1
```
