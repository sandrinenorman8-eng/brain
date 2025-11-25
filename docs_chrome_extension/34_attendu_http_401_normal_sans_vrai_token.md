# Attendu: HTTP 401 (normal sans vrai token)
```

**☐ Extension Configuration**
```javascript
// Console extension (chrome://extensions → Inspect views)
chrome.storage.sync.get(['backendUrl'], (data) => {
  console.log('Configured backend:', data.backendUrl);
});

chrome.storage.local.get(['authToken', 'tokenExpiry'], (data) => {
  console.log('Auth token:', data.authToken ? 'Present' : 'Missing');
  console.log('Token expiry:', new Date(data.tokenExpiry));
});
```

**☐ Permissions Manifest**
```json
// Vérifier dans chrome://extensions
{
  "host_permissions": [
    "https://your-actual-backend-domain.com/*" // ✅ Correspond à URL réelle
  ]
}
```

**☐ CSP Compliance**
```javascript
// Test dans background.js DevTools
fetch('https://your-backend.vercel.app/api/test')
  .then(r => r.json())
  .then(d => console.log('✅ CSP allows fetch:', d))
  .catch(e => console.error('❌ CSP blocks fetch:', e));
```

**☐ Network Analysis**

Ouvrir DevTools → Network
Filtrer: "api"
Déclencher action extension
Vérifier:

Status codes (200, 401, etc.)
Request headers (Authorization présent?)
Response headers (CORS présent?)
Timing (latence réseau)




**☐ Console Errors**

Extension console: chrome://extensions → background page
Popup console: Inspect popup
Options console: Inspect options page
Chercher:

CSP violations
CORS errors
Auth failures
Network timeouts



