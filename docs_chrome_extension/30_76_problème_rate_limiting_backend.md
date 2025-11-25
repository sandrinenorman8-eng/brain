### 7.6 Problème: Rate Limiting Backend

**Symptôme:**
Certaines requêtes retournent 429 Too Many Requests
Extension semble "lente" ou non-responsive
Pas de retry automatique

**Solution: Exponential Backoff avec Retry**
```javascript
// background.js - fonction fetch améliorée
async function callBackendWithRetry(endpoint, options = {}, attempt = 1) {
  const maxAttempts = 5;
  const baseDelay = 1000; // 1 seconde
  
  try {
    const baseUrl = await getBackendUrl();
    const token = await getAuthToken();
    
    const response = await fetch(`${baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
      }
    });
    
    // Success
    if (response.ok) {
      return await response.json();
    }
    
    // Rate limited - retry avec backoff
    if (response.status === 429 && attempt < maxAttempts) {
      const retryAfter = response.headers.get('Retry-After');
      const delay = retryAfter 
        ? parseInt(retryAfter) * 1000 
        : baseDelay * Math.pow(2, attempt - 1); // Exponential backoff
      
      console.log(`Rate limited. Retrying in ${delay}ms (attempt ${attempt}/${maxAttempts})`);
      
      await new Promise(resolve => setTimeout(resolve, delay));
      return callBackendWithRetry(endpoint, options, attempt + 1);
    }
    
    // Auth error - forcer re-login
    if (response.status === 401 || response.status === 403) {
      await chrome.storage.local.remove(['authToken', 'refreshToken']);
      throw new Error('AUTH_REQUIRED');
    }
    
    // Autre erreur
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    
  } catch (error) {
    // Network error - retry
    if (error.name === 'TypeError' && attempt < maxAttempts) {
      const delay = baseDelay * Math.pow(2, attempt - 1);
      console.log(`Network error. Retrying in ${delay}ms`);
      
      await new Promise(resolve => setTimeout(resolve, delay));
      return callBackendWithRetry(endpoint, options, attempt + 1);
    }
    
    throw error;
  }
}
```

**Backend: Implémenter Rate Limiting**
```javascript
const rateLimit = require('express-rate-limit');

// Configuration rate limiter
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Max 100 requêtes par fenêtre
  standardHeaders: true, // Retourner info dans headers
  legacyHeaders: false,
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too many requests',
      retryAfter: Math.ceil(req.rateLimit.resetTime / 1000)
    });
  }
});

// Appliquer à toutes routes API
app.use('/api/', apiLimiter);

// Rate limit spécifique pour auth (plus strict)
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true
});

app.use('/api/auth/', authLimiter);
```

---
