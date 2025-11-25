# 11.3 Scripts de Déploiement

## deploy-gae.sh

```bash
#!/bin/bash
set -e

echo "🚀 Deploying backend to Google App Engine..."

# Vérifier gcloud CLI installé
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install:"
    echo "https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Vérifier authentification
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo "❌ Not authenticated. Running gcloud auth login..."
    gcloud auth login
fi

# Vérifier projet configuré
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ No project configured. Please run:"
    echo "gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📦 Project: $PROJECT_ID"

# Déployer
cd backend/
echo "🔨 Deploying to App Engine..."
gcloud app deploy --quiet

# Récupérer URL déployée
URL=$(gcloud app browse --no-launch-browser 2>&1 | grep -o 'https://[^[:space:]]*')
echo "✅ Deployed to: $URL"

# Mettre à jour manifest extension
cd ../extension/
if [ -f "manifest.json" ]; then
    # Backup
    cp manifest.json manifest.json.bak
    
    # Remplacer URL
    sed -i.tmp "s|https://.*\.appspot\.com|$URL|g" manifest.json
    rm manifest.json.tmp 2>/dev/null || true
    
    echo "✅ Manifest updated with new URL"
else
    echo "⚠️  manifest.json not found in extension/"
fi

echo "✅ Deployment complete!"
echo "⚠️  Don't forget to update CSP in manifest.json if domain changed"
```

## test-backend.sh

```bash
#!/bin/bash

echo "🧪 Testing backend deployment..."

# Récupérer URL
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
REGION=$(gcloud app describe --format="value(locationId)" 2>/dev/null)
URL="https://${PROJECT_ID}.${REGION}.r.appspot.com"

echo "Testing: $URL/api/health"

# Test health endpoint
RESPONSE=$(curl -s -w "\n%{http_code}" "$URL/api/health")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Health check passed"
    echo "Response: $BODY"
else
    echo "❌ Health check failed (HTTP $HTTP_CODE)"
    echo "Response: $BODY"
    exit 1
fi

# Test CORS headers
echo ""
echo "🔍 Checking CORS headers..."
CORS_HEADER=$(curl -s -I "$URL/api/health" | grep -i "access-control-allow-origin")

if [ -n "$CORS_HEADER" ]; then
    echo "✅ CORS configured: $CORS_HEADER"
else
    echo "❌ CORS header missing!"
    exit 1
fi

echo ""
echo "✅ All tests passed!"
```

## rollback-gae.sh

```bash
#!/bin/bash
set -e

echo "⏪ Rolling back to previous version..."

# Lister les versions
echo "Available versions:"
gcloud app versions list

# Demander quelle version
read -p "Enter version to rollback to: " VERSION

# Migrer le trafic
gcloud app services set-traffic default --splits=$VERSION=1

echo "✅ Rolled back to version $VERSION"
```

## setup-gae.sh

```bash
#!/bin/bash
set -e

echo "🔧 Setting up Google App Engine project..."

# Vérifier gcloud
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Installing..."
    curl https://sdk.cloud.google.com | bash
    exec -l $SHELL
fi

# Login
echo "🔐 Authenticating..."
gcloud auth login

# Créer/sélectionner projet
read -p "Enter PROJECT_ID (or press Enter to create new): " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    read -p "Enter new project name: " PROJECT_NAME
    PROJECT_ID=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
    gcloud projects create $PROJECT_ID --name="$PROJECT_NAME"
fi

# Configurer projet
gcloud config set project $PROJECT_ID

# Activer APIs
echo "🔌 Enabling required APIs..."
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Créer App Engine
echo "🏗️  Creating App Engine application..."
read -p "Enter region (default: europe-west1): " REGION
REGION=${REGION:-europe-west1}

gcloud app create --region=$REGION

echo "✅ Setup complete!"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo ""
echo "Next steps:"
echo "1. cd backend/"
echo "2. gcloud app deploy"
```
