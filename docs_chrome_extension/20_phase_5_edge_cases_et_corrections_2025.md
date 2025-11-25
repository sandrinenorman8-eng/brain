## 7. PHASE 5 : EDGE CASES ET CORRECTIONS 2025 {#7-phase5}

### 7.1 Problème: URLs de Tunnel Dynamiques

**Symptôme:**
Extension garde en cache ancien hostname ngrok après redémarrage tunnel
Requêtes fetch échouent avec ERR_NAME_NOT_RESOLVED

**Cause:**
Service worker Chrome met en cache résolutions DNS et connexions

**Solution 1: Rechargement Extension Forcé**
```javascript
// options.js - après changement URL
saveUrlBtn.addEventListener('click', async () => {
  const newUrl = backendUrlInput.value.trim();
  await chrome.storage.sync.set({ backendUrl: newUrl });
  
  // CRITIQUE: Forcer reload service worker
  chrome.runtime.reload();
});
```

**Solution 2: Patterns Permissions Larges**
```json
// manifest.json - accepter tous sous-domaines ngrok
{
  "host_permissions": [
    "https://*.ngrok-free.app/*",
    "https://*.ngrok.io/*",
    "https://*.ngrok.app/*"
  ]
}
```

**Solution 3: Détection Changement URL**
```javascript
// background.js - listener changements storage
chrome.storage.onChanged.addListener((changes, area) => {
  if (area === 'sync' && changes.backendUrl) {
    console.log('Backend URL changed:', changes.backendUrl.newValue);
    
    // Invalider cache connexions
    chrome.webRequest.handlerBehaviorChanged(() => {
      console.log('Cache cleared');
    });
  }
});
```
