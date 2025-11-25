## 📋 RÉSUMÉ EXÉCUTIF

### Points Clés

**Backend:**
- Déploiement HTTPS obligatoire (Vercel/Render/Railway recommandés)
- CORS configuré pour `chrome-extension://*`
- Headers `Cache-Control: no-store` sur OPTIONS
- Authentification JWT (1h) + Refresh tokens (7j)
- Rate limiting actif

**Extension:**
- Manifest V3 avec `service_worker`
- Permissions: `storage`, `identity`, `host_permissions`
- CSP `connect-src` liste tous domaines backend
- OAuth via `chrome.identity.getAuthToken()`
- Tokens dans `chrome.storage.local` (jamais sync)

**Multi-Machines:**
- Publication Web Store → sync automatique
- Installation manuelle → transfert fichiers
- URL backend configurable via `options.html`
- Authentification séparée par machine

**Edge Cases 2025:**
- URLs tunnel dynamiques → `chrome.runtime.reload()`
- ID extension fixe → `key` dans manifest
- Cache CDN → `Cache-Control: no-store`
- CSP typos → validation stricte
- Service worker crashes → keep-alive pattern
