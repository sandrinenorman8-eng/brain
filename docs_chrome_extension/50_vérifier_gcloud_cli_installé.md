# Vérifier Google Cloud CLI installé

```bash
# Vérifier si gcloud est installé
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Installing..."
    
    # Windows
    # Télécharger depuis: https://cloud.google.com/sdk/docs/install
    
    # Linux/Mac
    curl https://sdk.cloud.google.com | bash
    exec -l $SHELL
fi

# Vérifier version
gcloud version

# Mettre à jour si nécessaire
gcloud components update
```
