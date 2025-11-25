const express = require('express');
const cors = require('cors');
const axios = require('axios');
const app = express();

// Configuration
const FLASK_LOCAL_URL = process.env.FLASK_URL || 'http://localhost:5008';
const TUNNEL_SECRET = process.env.TUNNEL_SECRET || 'change-me-in-production';

// CORS pour extensions Chrome
const corsOptions = {
  origin: [
    'chrome-extension://*',
    /^chrome-extension:\/\/[a-z]{32}$/
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Tunnel-Secret'],
  exposedHeaders: ['X-Total-Count'],
  maxAge: 86400
};

app.use(cors(corsOptions));
app.use(express.json({ limit: '100mb' }));
app.use(express.urlencoded({ limit: '100mb', extended: true }));

// Empêcher cache CDN des préflights
app.options('*', (req, res) => {
  res.set('Cache-Control', 'no-store');
  res.sendStatus(204);
});

// Middleware pour vérifier le secret tunnel (optionnel)
const checkTunnelSecret = (req, res, next) => {
  const secret = req.headers['x-tunnel-secret'];
  if (process.env.NODE_ENV === 'production' && secret !== TUNNEL_SECRET) {
    return res.status(403).json({ error: 'Invalid tunnel secret' });
  }
  next();
};

// Route de santé (ne passe pas par le proxy)
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: Date.now(),
    service: 'proxy-gae',
    version: '1.0.0',
    flask_url: FLASK_LOCAL_URL
  });
});

// Proxy TOUTES les requêtes vers Flask local
app.all('*', async (req, res) => {
  try {
    console.log(`[PROXY] ${req.method} ${req.path}`);
    
    // Construire l'URL Flask
    const flaskUrl = `${FLASK_LOCAL_URL}${req.path}`;
    
    // Faire la requête vers Flask
    const response = await axios({
      method: req.method,
      url: flaskUrl,
      data: req.body,
      params: req.query,
      headers: {
        'Content-Type': req.headers['content-type'] || 'application/json',
        'User-Agent': 'GAE-Proxy/1.0'
      },
      timeout: 30000,
      validateStatus: () => true // Accepter tous les status codes
    });
    
    // Retourner la réponse Flask
    res.status(response.status).json(response.data);
    
  } catch (error) {
    console.error('[PROXY ERROR]', error.message);
    
    if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({
        error: 'Flask backend not reachable',
        message: 'Make sure Flask is running on ' + FLASK_LOCAL_URL,
        hint: 'Run START.bat in deuxieme_cerveau folder'
      });
    }
    
    res.status(500).json({
      error: 'Proxy error',
      message: error.message
    });
  }
});

// Démarrer serveur
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`✅ Proxy server running on port ${PORT}`);
  console.log(`📡 Proxying to: ${FLASK_LOCAL_URL}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});
