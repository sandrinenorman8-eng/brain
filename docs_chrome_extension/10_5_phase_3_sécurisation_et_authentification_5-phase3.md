5. PHASE 3 : SÉCURISATION ET AUTHENTIFICATION {#5-phase3}
5.1 Principes de Sécurité Fondamentaux
❌ INTERDICTIONS ABSOLUES:

Jamais de secrets/API keys en dur dans le code
Jamais de tokens dans chrome.storage.sync (visible multi-devices)
Jamais d'URLs HTTP (non-chiffrées) en production

✅ BONNES PRATIQUES:

Tokens JWT courts (exp: 1h) avec refresh tokens
Stockage chrome.storage.local pour données sensibles
Headers Authorization: Bearer <token> pour authentification
Rotation automatique des tokens

5.2 Implémentation OAuth avec chrome.identity
Configuration OAuth (Google):

Créer projet sur Google Cloud Console
Activer API "Google+ API"
Créer OAuth 2.0 Client ID

Type: Chrome Extension
Authorized redirect URIs: https://<extension-id>.chromiumapp.org/



Code Authentification (options.js - complété):
javascript// Fonction OAuth complète
async function authenticateWithOAuth() {
  return new Promise((resolve, reject) => {
    chrome.identity.getAuthToken({ interactive: true }, async (token) => {
      if (chrome.runtime.lastError) {
        return reject(new Error(chrome.runtime.lastError.message));
      }
      
      if (!token) {
        return reject(new Error('No token received'));
      }
      
      try {
        // Échanger token Google contre token backend
        const backendUrl = await getBackendUrl();
        const response = await fetch(`${backendUrl}/api/auth/google`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ googleToken: token })
        });
        
        if (!response.ok) {
          throw new Error(`Auth failed: ${response.status}`);
        }
        
        const { jwtToken, refreshToken } = await response.json();
        
        // Stocker tokens
        await chrome.storage.local.set({
          authToken: jwtToken,
          refreshToken: refreshToken,
          tokenExpiry: Date.now() + 3600000 // 1h
        });
        
        resolve(jwtToken);
      } catch (error) {
        // Nettoyer token Google en cas d'échec
        chrome.identity.removeCachedAuthToken({ token }, () => {});
        reject(error);
      }
    });
  });
}

// Fonction: récupérer token (avec refresh automatique)
async function getAuthToken() {
  const { authToken, refreshToken, tokenExpiry } = await chrome.storage.local.get([
    'authToken',
    'refreshToken',
    'tokenExpiry'
  ]);
  
  // Token encore valide
  if (authToken && Date.now() < tokenExpiry - 60000) { // 1min marge
    return authToken;
  }
  
  // Refresh nécessaire
  if (refreshToken) {
    try {
      const backendUrl = await getBackendUrl();
      const response = await fetch(`${backendUrl}/api/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refreshToken })
      });
      
      if (response.ok) {
        const { jwtToken, newRefreshToken } = await response.json();
        
        await chrome.storage.local.set({
          authToken: jwtToken,
          refreshToken: newRefreshToken || refreshToken,
          tokenExpiry: Date.now() + 3600000
        });
        
        return jwtToken;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
    }
  }
  
  // Forcer ré-authentification
  throw new Error('AUTH_REQUIRED');
}
5.3 Backend: Validation JWT
Implémentation Node.js/Express:
javascriptconst jwt = require('jsonwebtoken');
const { OAuth2Client } = require('google-auth-library');

const JWT_SECRET = process.env.JWT_SECRET;
const REFRESH_SECRET = process.env.REFRESH_SECRET;
const googleClient = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

// Middleware: vérifier JWT
function authenticateJWT(req, res, next) {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  const token = authHeader.substring(7);
  
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(403).json({ error: 'Invalid token' });
  }
}

// Route: échange token Google
app.post('/api/auth/google', async (req, res) => {
  const { googleToken } = req.body;
  
  try {
    // Vérifier token Google
    const ticket = await googleClient.verifyIdToken({
      idToken: googleToken,
      audience: process.env.GOOGLE_CLIENT_ID
    });
    
    const payload = ticket.getPayload();
    const userId = payload.sub;
    const email = payload.email;
    
    // Créer JWT backend
    const jwtToken = jwt.sign(
      { userId, email },
      JWT_SECRET,
      { expiresIn: '1h' }
    );
    
    const refreshToken = jwt.sign(
      { userId, type: 'refresh' },
      REFRESH_SECRET,
      { expiresIn: '7d' }
    );
    
    res.json({ jwtToken, refreshToken });
  } catch (error) {
    res.status(401).json({ error: 'Invalid Google token' });
  }
});

// Route: refresh token
app.post('/api/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  
  try {
    const decoded = jwt.verify(refreshToken, REFRESH_SECRET);
    
    if (decoded.type !== 'refresh') {
      throw new Error('Invalid token type');
    }
    
    const jwtToken = jwt.sign(
      { userId: decoded.userId },
      JWT_SECRET,
      { expiresIn: '1h' }
    );
    
    res.json({ jwtToken });
  } catch (error) {
    res.status(403).json({ error: 'Invalid refresh token' });
  }
});

// Route protégée exemple
app.get('/api/user/profile', authenticateJWT, (req, res) => {
  res.json({
    userId: req.user.userId,
    email: req.user.email
  });
});
5.4 Content Security Policy (CSP) - Configuration Avancée
Problèmes Fréquents:

Typos dans connect-src bloquent silencieusement requêtes
Incohérence entre extension_pages et content_scripts
Oubli de domaines backend dans whitelist

Configuration Complète manifest.json:
json{
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'; connect-src 'self' https://your-backend.vercel.app https://*.ngrok-free.app https://*.render.com https://*.railway.app https://accounts.google.com https://oauth2.googleapis.com;",
    "content_scripts": "script-src 'self'; object-src 'self';"
  }
}
Points Critiques:

Chaque domaine backend doit apparaître dans connect-src
Inclure domaines OAuth (Google, etc.)
Pas d'espaces après points-virgules
Tester avec Console DevTools → violations CSP visibles

