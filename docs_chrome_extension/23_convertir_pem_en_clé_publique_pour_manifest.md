# Convertir .pem en clé publique pour manifest
openssl rsa -in extension-key.pem -pubout -outform DER | base64 -w 0

# Copier output (commence par "MII...")
```

**Étape 7.2.3 : Ajouter au Manifest**
```json
{
  "manifest_version": 3,
  "name": "Extension Multi-Backend",
  "key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...", // Clé publique complète
  ...
}
```

**Avantages:**
✅ ID extension fixe: `abcdefghijklmnopqrstuvwxyzabcdef`  
✅ Pas de re-signature par Web Store  
✅ CORS backend stable  
✅ OAuth redirect URIs permanents  

**⚠️ SÉCURITÉ:**

Clé privée (.pem): SAUVEGARDER hors repo Git
Ne JAMAIS commit .pem
Stocker dans gestionnaire secrets (1Password, Vault)

