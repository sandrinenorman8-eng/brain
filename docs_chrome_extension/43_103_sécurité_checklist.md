### 10.3 Sécurité Checklist
☐ Toutes URLs backend en HTTPS (pas HTTP)
☐ Tokens JWT stockés dans storage.local (pas sync)
☐ Refresh tokens implémentés
☐ Token expiration gérée automatiquement
☐ Pas de secrets/API keys dans manifest
☐ CSP empêche inline scripts
☐ CSP connect-src liste blanche domaines
☐ CORS backend limite origines chrome-extension://
☐ Backend valide tokens JWT sur chaque requête
☐ Rate limiting actif côté backend
☐ Logs n'exposent pas données sensibles
☐ Extension key réservée (ID fixe)
