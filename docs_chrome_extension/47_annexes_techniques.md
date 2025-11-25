## 11. ANNEXES TECHNIQUES {#11-annexes}

### 11.1 Exemple Backend Complet (Node.js/Express)
```javascript
// server.js
const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const { OAuth2Client } = require('google-auth-library');
const rateLimit = require('express-rate-limit');

const app = express();
const PORT = process.env.PORT || 3000;

// Configuration
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-prod';
const REFRESH_SECRET = process.env.REFRESH_SECRET || 'refresh-secret-change';
const GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID;

const googleClient = new OAuth2Client(GOOGLE_CLIENT_ID);

// Middleware: CORS avancé
app.use((req, res, next) => {
  const origin = req.get('origin');
  
  // Accepter extensions Chrome + domaines web spécifiques
  if (origin && (
    origin.startsWith('chrome-extension://') ||
    origin === 'https://your-frontend.com'
  )) {
    res.set('Access-Control-Allow-Origin', origin);
  }
  
  res.set('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type,Authorization');
  res.set('Access-Control-Allow-Credentials', 'true');
  res.set('Access-Control-Max-Age', '86400');
  
  // OPTIONS preflight
  if (req.method === 'OPTIONS') {
    res.set('Cache-Control', 'no-store, no-cache, must-revalidate');
    res.set('Pragma', 'no-cache');
    return res.sendStatus(204);
  }
  
  next();
});

app.use(express.json());

// Rate limiting
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too many requests',
      retryAfter: Math.ceil(req.rateLimit.resetTime / 1000)
    });
  }
});

app.use('/api/', apiLimiter);

// Middleware: Authentification JWT
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
    return res.status(403).json({ error: 'Invalid or expired token' });
  }
}

// Routes

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: Date.now(),
    version: '1.0.0'
  });
});

// Authentification Google
app.post('/api/auth/google', async (req, res) => {
  const { googleToken } = req.body;
  
  if (!googleToken) {
    return res.status(400).json({ error: 'Google token required' });
  }
  
  try {
    // Vérifier token Google
    const ticket = await googleClient.verifyIdToken({
      idToken: googleToken,
      audience: GOOGLE_CLIENT_ID
    });
    
    const payload = ticket.getPayload();
    const userId = payload.sub;
    const email = payload.email;
    const name = payload.name;
    
    // Créer/récupérer utilisateur en DB (simulé ici)
    const user = {
      id: userId,
      email,
      name
    };
    
    // Générer JWT
    const jwtToken = jwt.sign(
      { userId, email, name },
      JWT_SECRET,
      { expiresIn: '1h' }
    );
    
    const refreshToken = jwt.sign(
      { userId, type: 'refresh' },
      REFRESH_SECRET,
      { expiresIn: '7d' }
    );
    
    res.json({
      jwtToken,
      refreshToken,
      user
    });
    
  } catch (error) {
    console.error('Auth error:', error);
    res.status(401).json({ error: 'Invalid Google token' });
  }
});

// Refresh token
app.post('/api/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  
  if (!refreshToken) {
    return res.status(400).json({ error: 'Refresh token required' });
  }
  
  try {
    const decoded = jwt.verify(refreshToken, REFRESH_SECRET);
    
    if (decoded.type !== 'refresh') {
      throw new Error('Invalid token type');
    }
    
    // Générer nouveau JWT
    const jwtToken = jwt.sign(
      { userId: decoded.userId },
      JWT_SECRET,
      { expiresIn: '1h' }
    );
    
    // Optionnel: rotation refresh token
    const newRefreshToken = jwt.sign(
      { userId: decoded.userId, type: 'refresh' },
      REFRESH_SECRET,
      { expiresIn: '7d' }
    );
    
    res.json({
      jwtToken,
      newRefreshToken
    });
    
  } catch (error) {
    console.error('Refresh error:', error);
    res.status(403).json({ error: 'Invalid refresh token' });
  }
});

// Route protégée: Profil utilisateur
app.get('/api/user/profile', authenticateJWT, (req, res) => {
  res.json({
    userId: req.user.userId,
    email: req.user.email,
    name: req.user.name
  });
});

// Route protégée: Exemple API
app.post('/api/data', authenticateJWT, async (req, res) => {
  try {
    const { action, payload } = req.body;
    
    // Logique métier ici
    const result = {
      success: true,
      action,
      userId: req.user.userId,
      timestamp: Date.now()
    };
    
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Telemetry (optionnel)
app.post('/api/telemetry/errors', authenticateJWT, (req, res) => {
  const errorData = req.body;
  
  // Logger ou stocker en DB
  console.error('Client error:', {
    userId: req.user.userId,
    error: errorData
  });
  
  res.sendStatus(204);
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// Démarrage
app.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});

module.exports = app;
```
