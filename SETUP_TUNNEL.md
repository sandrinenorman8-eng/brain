# Configuration Tunnel Flask → GAE

## Architecture

```
Extension Chrome
    ↓
Backend GAE (proxy)
    ↓ (via tunnel)
Flask Local (ton app)
```

## Étape 1 : Installer Cloudflare Tunnel

```bash
# Windows
winget install --id Cloudflare.cloudflared
```

## Étape 2 : Créer le Tunnel

```bash
# Se connecter
cloudflared tunnel login

# Créer tunnel
cloudflared tunnel create memobrik-tunnel

# Noter le Tunnel ID affiché
```

## Étape 3 : Configurer le Tunnel

Crée `C:\Users\TON_USER\.cloudflared\config.yml` :

```yaml
tunnel: TUNNEL_ID_ICI
credentials-file: C:\Users\TON_USER\.cloudflared\TUNNEL_ID.json

ingress:
  - hostname: memobrik.ton-domaine.com
    service: http://localhost:5008
  - service: http_status:404
```

## Étape 4 : Démarrer le Tunnel

```bash
cloudflared tunnel run memobrik-tunnel
```

Ou en service Windows :
```bash
cloudflared service install
```

## Étape 5 : Mettre à Jour le Backend GAE

Dans `backend/app.yaml`, ajoute :

```yaml
env_variables:
  FLASK_URL: "https://memobrik.ton-domaine.com"
  TUNNEL_SECRET: "ton-secret-securise"
```

## Étape 6 : Redéployer

```bash
cd backend
gcloud app deploy
```

## Alternative : ngrok (Plus Simple)

```bash
# Installer ngrok
winget install ngrok

# Démarrer tunnel
ngrok http 5008

# Copier l'URL https://xxx.ngrok-free.app
# Mettre dans backend/app.yaml :
# FLASK_URL: "https://xxx.ngrok-free.app"
```

## Test

1. Lance Flask : `START.bat` dans deuxieme_cerveau
2. Lance tunnel : `cloudflared tunnel run` ou `ngrok http 5008`
3. Backend GAE proxy automatiquement vers Flask
4. Extension Chrome → GAE → Tunnel → Flask Local

## Avantages

- ✅ Flask reste en local (pas de migration)
- ✅ Toutes les fonctionnalités préservées
- ✅ Accès fichiers locaux OK
- ✅ Extension fonctionne partout
- ✅ Gratuit (Cloudflare) ou $5/mois (ngrok)
