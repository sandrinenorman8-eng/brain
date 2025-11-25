2. ARCHITECTURE GLOBALE {#2-architecture}
2.1 Composants Principaux
┌─────────────────┐         HTTPS          ┌──────────────────┐
│   Extension     │◄─────────────────────►│   Backend        │
│   Chrome        │   (fetch + auth)       │   Public         │
│                 │                        │   (Cloud/Tunnel) │
│ - background.js │                        │                  │
│ - options.html  │                        │ - API Routes     │
│ - manifest.json │                        │ - CORS Config    │
└─────────────────┘                        └──────────────────┘
        │
        │ chrome.storage.sync
        ▼
┌─────────────────┐
│  Configuration  │
│  - backendUrl   │
│  - auth tokens  │
└─────────────────┘
2.2 Flux de Données

Utilisateur configure l'URL backend via options.html
Extension stocke l'URL dans chrome.storage.sync
Service worker (background.js) récupère l'URL et établit connexions
Authentification OAuth via chrome.identity
Tokens stockés dans chrome.storage.local
Requêtes API signées avec tokens JWT

