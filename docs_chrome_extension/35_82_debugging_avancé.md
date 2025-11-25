### 8.2 Debugging Avancé

**Scenario 1: "Extension ne répond pas"**
```javascript
// Ajouter logging détaillé background.js
const DEBUG = true;

function log(...args) {
  if (DEBUG) {
    console.log('[DEBUG]', new Date().toISOString(), ...args);
  }
}

// Wrapper fetch avec logs
async function debugFetch(url, options) {
  log('Fetch started:', url, options);
  
  try {
    const start = performance.now();
    const response = await fetch(url, options);
    const duration = performance.now() - start;
    
    log('Fetch completed:', {
      url,
      status: response.status,
      duration: `${duration.toFixed(2)}ms`,
      headers: Object.fromEntries(response.headers)
    });
    
    return response;
  } catch (error) {
    log('Fetch failed:', url, error);
    throw error;
  }
}
```

**Scenario 2: "CORS errors persistants"**
```javascript
// Test CORS depuis extension
async function diagnoseCORS() {
  const backendUrl = await getBackendUrl();
  const testUrl = `${backendUrl}/api/health`;
  
  console.group('CORS Diagnosis');
  
  // Test 1: Simple GET
  try {
    const r1 = await fetch(testUrl);
    console.log('✅ Simple GET:', r1.status);
    console.log('Headers:', Object.fromEntries(r1.headers));
  } catch (e) {
    console.error('❌ Simple GET failed:', e);
  }
  
  // Test 2: GET avec headers customs
  try {
    const r2 = await fetch(testUrl, {
      headers: { 'Authorization': 'Bearer test' }
    });
    console.log('✅ GET with auth:', r2.status);
  } catch (e) {
    console.error('❌ GET with auth failed:', e);
  }
  
  // Test 3: POST (déclenche preflight)
  try {
    const r3 = await fetch(`${backendUrl}/api/test`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ test: true })
    });
    console.log('✅ POST request:', r3.status);
  } catch (e) {
    console.error('❌ POST failed:', e);
  }
  
  console.groupEnd();
}

// Exécuter au chargement extension
diagnoseCORS();
```

**Scenario 3: "Token expiré non détecté"**
```javascript
// Middleware validation token automatique
async function fetchWithAuthCheck(url, options = {}) {
  try {
    const token = await getAuthToken(); // Peut throw AUTH_REQUIRED
    
    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${token}`
      }
    });
    
    // Backend retourne 401 - forcer refresh
    if (response.status === 401) {
      console.warn('Token rejected by backend, clearing...');
      await chrome.storage.local.remove(['authToken', 'refreshToken']);
      throw new Error('AUTH_REQUIRED');
    }
    
    return response;
    
  } catch (error) {
    if (error.message === 'AUTH_REQUIRED') {
      // Notifier utilisateur
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon48.png',
        title: 'Authentification Requise',
        message: 'Veuillez vous reconnecter'
      });
      
      // Ouvrir page options
      chrome.runtime.openOptionsPage();
    }
    throw error;
  }
}
```
