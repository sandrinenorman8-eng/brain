## 10. CHECKLIST FINALE {#10-checklist}

### 10.1 Backend Checklist
☐ Déployé sur plateforme HTTPS (Vercel/Render/Railway/GAE)
☐ URL publique stable obtenue
☐ Variables d'environnement configurées (JWT_SECRET, DB_URL)
☐ CORS configuré pour chrome-extension://*
☐ Headers CORS incluent: Allow-Origin, Allow-Methods, Allow-Headers
☐ Cache-Control: no-store sur OPTIONS requests
☐ Route /api/health répond 200
☐ Route /api/auth/google implémentée
☐ Route /api/auth/refresh implémentée
☐ JWT expiration: 1h
☐ Refresh token expiration: 7d
☐ Rate limiting configuré (100 req/15min)
☐ Logging errors actif
☐ Tests endpoint avec curl réussis
