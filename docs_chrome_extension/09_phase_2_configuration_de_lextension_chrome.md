## 4. PHASE 2 : CONFIGURATION DE L'EXTENSION CHROME {#4-phase2}

### 4.1 Structure des Fichiers
```
extension/
├── manifest.json          # Configuration principale
├── background.js          # Service worker
├── options.html           # Page de configuration
├── options.js             # Logique configuration
├── popup.html             # Interface popup (optionnel)
├── popup.js               # Logique popup
└── icons/
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
4.2 Configuration manifest.json (Manifest V3)
json{
  "manifest_version": 3,
  "name": "Extension Multi-Backend",
  "version": "1.0.0",
  "description": "Extension connectée à backend distant configurable",
  
  "permissions": [
    "storage",
    "identity"
  ],
  
  "host_permissions": [
    "https://your-backend.vercel.app/*",
    "https://*.ngrok-free.app/*",
    "https://*.render.com/*",
    "https://*.railway.app/*"
  ],
  
  "background": {
    "service_worker": "background.js",
    "type": "module"
  },
  
  "options_ui": {
    "page": "options.html",
    "open_in_tab": false
  },
  
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'; connect-src 'self' https://your-backend.vercel.app https://*.ngrok-free.app https://*.render.com https://*.railway.app;"
  },
  
  "oauth2": {
    "client_id": "YOUR_OAUTH_CLIENT_ID.apps.googleusercontent.com",
    "scopes": ["openid", "email", "profile"]
  },
  
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
4.3 Implémentation Service Worker (background.js)
javascript// background.js - Service Worker
const DEFAULT_BACKEND_URL = 'https://your-backend.vercel.app';

// Fonction utilitaire: récupérer URL backend
async function getBackendUrl() {
  const { backendUrl } = await chrome.storage.sync.get('backendUrl');
  return backendUrl || DEFAULT_BACKEND_URL;
}

// Fonction utilitaire: récupérer token auth
async function getAuthToken() {
  const { authToken } = await chrome.storage.local.get('authToken');
  return authToken;
}

// Fonction principale: appel API backend
async function callBackend(endpoint, options = {}) {
  const baseUrl = await getBackendUrl();
  const token = await getAuthToken();
  
  const url = `${baseUrl}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  try {
    const response = await fetch(url, {
      ...options,
      headers,
      credentials: 'include'
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Backend call failed:', error);
    
    // Retry logic avec exponential backoff
    if (options.retry > 0) {
      await new Promise(resolve => setTimeout(resolve, 1000 * (4 - options.retry)));
      return callBackend(endpoint, { ...options, retry: options.retry - 1 });
    }
    
    throw error;
  }
}

// Listener messages depuis popup/content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'apiCall') {
    callBackend(message.endpoint, { 
      method: message.method || 'GET',
      body: message.body ? JSON.stringify(message.body) : undefined,
      retry: 3
    })
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    
    return true; // Indique réponse asynchrone
  }
});

// Installation: vérifier configuration
chrome.runtime.onInstalled.addListener(async ({ reason }) => {
  if (reason === 'install') {
    // Ouvrir page options au premier lancement
    chrome.runtime.openOptionsPage();
  }
  
  // Vérifier santé backend
  try {
    const health = await callBackend('/api/health', { retry: 1 });
    console.log('Backend health check:', health);
  } catch (error) {
    console.warn('Backend unreachable at startup:', error);
  }
});
4.4 Page de Configuration (options.html)
html<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Extension Configuration</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      padding: 20px;
      max-width: 600px;
      margin: 0 auto;
    }
    .config-section {
      margin: 20px 0;
      padding: 15px;
      border: 1px solid #ddd;
      border-radius: 8px;
    }
    label {
      display: block;
      margin-bottom: 8px;
      font-weight: bold;
    }
    input[type="text"] {
      width: 100%;
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 14px;
    }
    button {
      background: #4285f4;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 14px;
      margin-top: 10px;
    }
    button:hover {
      background: #357ae8;
    }
    .status {
      margin-top: 10px;
      padding: 10px;
      border-radius: 4px;
      display: none;
    }
    .status.success {
      background: #d4edda;
      color: #155724;
      border: 1px solid #c3e6cb;
    }
    .status.error {
      background: #f8d7da;
      color: #721c24;
      border: 1px solid #f5c6cb;
    }
  </style>
</head>
<body>
  <h1>⚙️ Configuration Extension</h1>
  
  <div class="config-section">
    <h2>Backend URL</h2>
    <label for="backendUrl">URL du Backend (HTTPS uniquement):</label>
    <input 
      type="text" 
      id="backendUrl" 
      placeholder="https://your-backend.vercel.app"
      pattern="https://.*"
    >
    <button id="saveUrl">Enregistrer l'URL</button>
    <button id="testConnection">Tester la Connexion</button>
    <div id="urlStatus" class="status"></div>
  </div>
  
  <div class="config-section">
    <h2>Authentification</h2>
    <button id="loginBtn">Se Connecter (OAuth)</button>
    <button id="logoutBtn">Se Déconnecter</button>
    <div id="authStatus" class="status"></div>
  </div>
  
  <script src="options.js"></script>
</body>
</html>
4.5 Logique Configuration (options.js)
javascript// options.js
document.addEventListener('DOMContentLoaded', async () => {
  const backendUrlInput = document.getElementById('backendUrl');
  const saveUrlBtn = document.getElementById('saveUrl');
  const testConnectionBtn = document.getElementById('testConnection');
  const loginBtn = document.getElementById('loginBtn');
  const logoutBtn = document.getElementById('logoutBtn');
  const urlStatus = document.getElementById('urlStatus');
  const authStatus = document.getElementById('authStatus');
  
  // Charger URL sauvegardée
  const { backendUrl } = await chrome.storage.sync.get('backendUrl');
  if (backendUrl) {
    backendUrlInput.value = backendUrl;
  }
  
  // Sauvegarder URL
  saveUrlBtn.addEventListener('click', async () => {
    const url = backendUrlInput.value.trim();
    
    // Validation
    if (!url.startsWith('https://')) {
      showStatus(urlStatus, 'Seules les URLs HTTPS sont autorisées', 'error');
      return;
    }
    
    try {
      new URL(url); // Vérifier format URL
      await chrome.storage.sync.set({ backendUrl: url });
      showStatus(urlStatus, 'URL enregistrée avec succès', 'success');
      
      // Recharger service worker pour appliquer changements
      chrome.runtime.reload();
    } catch (error) {
      showStatus(urlStatus, `URL invalide: ${error.message}`, 'error');
    }
  });
  
  // Tester connexion
  testConnectionBtn.addEventListener('click', async () => {
    const url = backendUrlInput.value.trim();
    
    try {
      const response = await fetch(`${url}/api/health`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (response.ok) {
        const data = await response.json();
        showStatus(urlStatus, `✅ Backend accessible: ${data.status}`, 'success');
      } else {
        showStatus(urlStatus, `❌ Erreur HTTP ${response.status}`, 'error');
      }
    } catch (error) {
      showStatus(urlStatus, `❌ Connexion impossible: ${error.message}`, 'error');
    }
  });
  
  // Authentification OAuth
  loginBtn.addEventListener('click', async () => {
    try {
      const token = await authenticateWithOAuth();
      await chrome.storage.local.set({ authToken: token });
      showStatus(authStatus, '✅ Authentification réussie', 'success');
    } catch (error) {
      showStatus(authStatus, `❌ Échec auth: ${error.message}`, 'error');
    }
  });
  
  // Déconnexion
  logoutBtn.addEventListener('click', async () => {
    await chrome.storage.local.remove('authToken');
    showStatus(authStatus, 'Déconnecté', 'success');
  });
});

// Fonction utilitaire: afficher message status
function showStatus(element, message, type) {
  element.textContent = message;
  element.className = `status ${type}`;
  element.style.display = 'block';
  
  setTimeout(() => {
    element.style.display = 'none';
  }, 5000);
}

// Fonction OAuth (voir section 5 pour implémentation complète)
async function authenticateWithOAuth() {
  // Implémentation dans section Authentification
  throw new Error('À implémenter');
}
