# Récupérer l'URL déployée sur Google App Engine
PROJECT_ID=$(gcloud config get-value project)
REGION=$(gcloud app describe --format="value(locationId)")
URL="https://${PROJECT_ID}.${REGION}.r.appspot.com"
echo "Backend URL: $URL"

# Exemple: https://my-backend-123456.ew.r.appspot.com
Étape 1.4 : Variables d'Environnement

Méthode 1 - Dans app.yaml:
```yaml
env_variables:
  JWT_SECRET: "votre-secret-ici"
  DATABASE_URL: "postgresql://..."
```

Méthode 2 - Secret Manager (Recommandé):
```bash
# Créer secrets
echo -n "votre-secret-ici" | gcloud secrets create jwt-secret --data-file=-
echo -n "postgresql://..." | gcloud secrets create database-url --data-file=-

# Donner accès à App Engine
gcloud secrets add-iam-policy-binding jwt-secret \
  --member="serviceAccount:YOUR_PROJECT_ID@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```
3.3 Configuration CORS Backend
Implémentation Node.js/Express:
javascriptconst express = require('express');
const cors = require('cors');
const app = express();

// Configuration CORS pour Extension Chrome
const corsOptions = {
  origin: [
    'chrome-extension://*', // Accepter toutes extensions (dev)
    /^chrome-extension:\/\/[a-z]{32}$/ // Pattern ID extension
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  exposedHeaders: ['X-Total-Count'],
  maxAge: 86400 // 24h cache préflight
};

app.use(cors(corsOptions));

// CRITIQUE: Empêcher cache CDN des préflights
app.options('*', (req, res) => {
  res.set('Cache-Control', 'no-store');
  res.sendStatus(204);
});

// Route de santé
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: Date.now() });
});

app.listen(process.env.PORT || 3000);
3.4 Validation de l'Accessibilité
Test Endpoint avec curl:
```bash
# Vérifier HTTPS et headers
curl -I https://YOUR_PROJECT_ID.REGION.r.appspot.com/api/health

# Test complet
curl https://YOUR_PROJECT_ID.REGION.r.appspot.com/api/health
```
