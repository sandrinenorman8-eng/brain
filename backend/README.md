# Backend Google App Engine

## Déploiement Rapide

```bash
# 1. Installer dépendances (local)
npm install

# 2. Tester local
npm start
# Ouvrir: http://localhost:8080/api/health

# 3. Déployer sur GAE
gcloud app deploy

# 4. Récupérer URL
gcloud app browse
```

## Endpoints

- `GET /api/health` - Health check
- `GET /api/test` - Test endpoint
- `POST /api/data` - Recevoir données de l'extension

## URL Production

Format: `https://PROJECT_ID.REGION.r.appspot.com`

Exemple: `https://my-project-123456.ew.r.appspot.com`
