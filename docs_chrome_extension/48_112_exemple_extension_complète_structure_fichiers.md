### 11.2 Exemple Extension Complète (Structure Fichiers)

**manifest.json:**
```json
{
  "manifest_version": 3,
  "name": "Multi-Backend Extension",
  "version": "1.0.0",
  "description": "Extension Chrome connectée à backend distant configurable",
  "permissions": ["storage", "identity", "notifications"],
  "host_permissions": [
    "https://your-backend.vercel.app/*",
    "https://*.ngrok-free.app/*"
  ],
  "background": {
    "service_worker": "background.js",
    "type": "module"
  },
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "options_ui": {
    "page": "options.html",
    "open_in_tab": false
  },
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'; connect-src 'self' https://your-backend.vercel.app https://*.ngrok-free.app https://accounts.google.com;"
  },
  "oauth2": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "scopes": ["openid", "email", "profile"]
  },
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
```

**popup.html:**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {
      width: 300px;
      padding: 15px;
      font-family: Arial, sans-serif;
    }
    .status {
      padding: 10px;
      margin: 10px 0;
      border-radius: 4px;
    }
    .status.connected {
      background: #d4edda;
      color: #155724;
    }
    .status.disconnected {
      background: #f8d7da;
      color: #721c24;
    }
    button {
      width: 100%;
      padding: 10px;
      margin: 5px 0;
      border: none;
      border-radius: 4px;
      background: #4285f4;
      color: white;
      cursor: pointer;
    }
    button:hover {
      background: #357ae8;
    }
  </style>
</head>
<body>
  <h2>🔌 Extension Status</h2>
  <div id="status" class="status disconnected">Vérification...</div>
  <button id="testConnection">Tester Connexion</button>
  <button id="openOptions">Paramètres</button>
  <div id="result"></div>
  <script src="popup.js"></script>
</body>
</html>
```

**popup.js:**
```javascript
document.addEventListener('DOMContentLoaded', async () => {
  const statusDiv = document.getElementById('status');
  const resultDiv = document.getElementById('result');
  
  // Vérifier status initial
  const { backendUrl } = await chrome.storage.sync.get('backendUrl');
  const { authToken } = await chrome.storage.local.get('authToken');
  
  if (!backendUrl) {
    statusDiv.textContent = '⚠️ Backend non configuré';
    statusDiv.className = 'status disconnected';
  } else if (!authToken) {
    statusDiv.textContent = '⚠️ Non authentifié';
    statusDiv.className = 'status disconnected';
  } else {
    statusDiv.textContent = '✅ Connecté';
    statusDiv.className = 'status connected';
  }
  
  // Test connexion
  document.getElementById('testConnection').addEventListener('click', async () => {
    resultDiv.textContent = 'Test en cours...';
    
    try {
      const response = await chrome.runtime.sendMessage({
        action: 'apiCall',
        endpoint: '/api/health',
        method: 'GET'
      });
      
      if (response.success) {
        resultDiv.textContent = `✅ Backend OK: ${response.data.status}`;
        statusDiv.textContent = '✅ Connecté';
        statusDiv.className = 'status connected';
      } else {
        resultDiv.textContent = `❌ Erreur: ${response.error}`;
      }
    } catch (error) {
      resultDiv.textContent = `❌ Erreur: ${error.message}`;
    }
  });
  
  // Ouvrir options
  document.getElementById('openOptions').addEventListener('click', () => {
    chrome.runtime.openOptionsPage();
  });
});
```
