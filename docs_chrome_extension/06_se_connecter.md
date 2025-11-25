# Se connecter à Google Cloud
gcloud auth login

# Sélectionner le projet
gcloud config set project YOUR_PROJECT_ID

# Initialiser App Engine
cd /path/to/backend
gcloud app create --region=europe-west1
Étape 1.2 : Configuration
json// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "index.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "index.js"
    }
  ],
  "env": {
    "NODE_ENV": "production",
    "JWT_SECRET": "@jwt-secret"
  }
}
Étape 1.3 : Déploiement
bash# Déployer en production
vercel --prod
