### 7.2 Problème: ID Extension Changeant

**Symptôme:**
Extension re-signée par Web Store a nouvel ID
Backend whitelist CORS obsolète
chrome-extension://OLD_ID → chrome-extension://NEW_ID

**Cause:**
Chrome Web Store peut re-signer extension lors mises à jour si clé privée non fournie

**Solution: Réservation ID Permanent**

**Étape 7.2.1 : Générer Paire Clés**
```bash