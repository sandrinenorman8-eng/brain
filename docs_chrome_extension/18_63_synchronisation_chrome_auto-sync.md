### 6.3 Synchronisation Chrome (Auto-sync)

**Activation Sync:**

Paramètres Chrome → Connexion
Se connecter avec compte Google
Activer "Synchronisation"
Cocher "Extensions"


**Comportement:**
- Extensions installées depuis Web Store → sync automatique
- Extensions chargées manuellement → PAS de sync (rester en local)
- Paramètres `chrome.storage.sync` → sync entre appareils
- Paramètres `chrome.storage.local` → local uniquement

**⚠️ ATTENTION:**
```javascript
// ❌ NE PAS stocker dans sync:
chrome.storage.sync.set({ authToken: 'secret' }); // DANGEREUX!

// ✅ Stocker dans local:
chrome.storage.local.set({ authToken: 'secret' }); // CORRECT
```
