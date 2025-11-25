### 9.2 Workflow Authentification
┌─────────────┐
│   Utilisateur│
│  Clique Login│
└──────┬──────┘
│
▼
┌──────────────────────────────────┐
│ Extension: chrome.identity.      │
│ getAuthToken({ interactive: true})│
└──────┬────────────────────────────┘
│
▼
┌──────────────────────┐
│ Google OAuth Consent │
│ (popup navigateur)   │
└──────┬───────────────┘
│
▼
┌─────────────────────────────┐
│ Google retourne token OAuth │
└──────┬──────────────────────┘
│
▼
┌──────────────────────────────────┐
│ Extension envoie token à Backend │
│ POST /api/auth/google            │
└──────┬──────────────────────────┘
│
▼
┌───────────────────────────────────┐
│ Backend vérifie token Google      │
│ Génère JWT + Refresh Token        │
└──────┬────────────────────────────┘
│
▼
┌────────────────────────────────────┐
│ Extension stocke tokens            │
│ chrome.storage.local               │
└──────┬─────────────────────────────┘
│
▼
┌────────────────────────┐
│ Requêtes API Signées   │
│ Authorization: Bearer  │
└────────────────────────┘
