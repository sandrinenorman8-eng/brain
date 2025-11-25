# Récupérer URL déployée sur Google App Engine

```bash
# Méthode 1 : Ouvrir dans le navigateur
gcloud app browse

# Méthode 2 : Récupérer l'URL programmatiquement
PROJECT_ID=$(gcloud config get-value project)
REGION=$(gcloud app describe --format="value(locationId)")
URL="https://${PROJECT_ID}.${REGION}.r.appspot.com"
echo "✅ Backend URL: $URL"

# Méthode 3 : Depuis la console
# https://console.cloud.google.com/appengine

# Mettre à jour manifest extension
cd ../extension/
sed -i "s|https://.*\.appspot\.com|$URL|g" manifest.json

echo "✅ Manifest updated with new URL"
echo "⚠️  Don't forget to update CSP in manifest.json if domain changed"
```

## Format de l'URL

L'URL suit le pattern :
```
https://PROJECT_ID.REGION_ID.r.appspot.com
```

Exemples :
- `https://my-backend-123456.ew.r.appspot.com` (Europe West)
- `https://my-backend-123456.uc.r.appspot.com` (US Central)

## Domaine Personnalisé (Optionnel)

```bash
# Mapper un domaine personnalisé
gcloud app domain-mappings create api.mondomaine.com

# Vérifier les mappings
gcloud app domain-mappings list
```
