### 9.4 Routine Conditionnelle: Gestion Token
```javascript
async function getValidToken() {
  // Checkpoint 1: Token existe?
  const { authToken, tokenExpiry } = await chrome.storage.local.get([
    'authToken',
    'tokenExpiry'
  ]);
  
  if (!authToken) {
    // Node 1: Pas de token → Authentification
    throw new Error('AUTH_REQUIRED');
  }
  
  // Checkpoint 2: Token encore valide?
  const now = Date.now();
  const expiryWithMargin = tokenExpiry - (5 * 60 * 1000); // 5min marge
  
  if (now < expiryWithMargin) {
    // Node 2: Token valide → Retourner
    return authToken;
  }
  
  // Checkpoint 3: Refresh token disponible?
  const { refreshToken } = await chrome.storage.local.get('refreshToken');
  
  if (!refreshToken) {
    // Node 3: Pas de refresh → Ré-authentification
    await chrome.storage.local.remove(['authToken', 'tokenExpiry']);
    throw new Error('AUTH_REQUIRED');
  }
  
  // Node 4: Tenter refresh
  try {
    const backendUrl = await getBackendUrl();
    const response = await fetch(`${backendUrl}/api/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refreshToken })RetryPContinue});
if (!response.ok) {
  throw new Error('Refresh failed');
}

const { jwtToken, newRefreshToken } = await response.json();

// Node 5: Sauvegarder nouveau token
await chrome.storage.local.set({
  authToken: jwtToken,
  refreshToken: newRefreshToken || refreshToken,
  tokenExpiry: now + (3600 * 1000) // 1h
});

return jwtToken;
} catch (error) {
// Node 6: Refresh échoué → Forcer ré-auth
await chrome.storage.local.remove([
'authToken',
'refreshToken',
'tokenExpiry'
]);
throw new Error('AUTH_REQUIRED');
}
}

---
