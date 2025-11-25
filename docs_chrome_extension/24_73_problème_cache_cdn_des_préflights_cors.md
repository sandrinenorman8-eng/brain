### 7.3 Problème: Cache CDN des Préflights CORS

**Symptôme:**
Modifications CORS backend ne s'appliquent pas
OPTIONS requests retournent anciennes réponses
Extension bloquée par erreur CORS malgré config correcte

**Cause:**
CloudFront, Cloudflare, Fastly mettent en cache réponses OPTIONS (préflight)

**Solution Backend:**
```javascript
// Express middleware CORS amélioré
app.use((req, res, next) => {
  res.set('Access-Control-Allow-Origin', req.get('origin') || '*');
  res.set('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type,Authorization');
  res.set('Access-Control-Allow-Credentials', 'true');
  res.set('Access-Control-Max-Age', '86400'); // Cache navigateur: 24h
  
  // CRITIQUE: Empêcher cache CDN
  if (req.method === 'OPTIONS') {
    res.set('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
    res.set('Pragma', 'no-cache');
    res.set('Expires', '0');
    res.set('Surrogate-Control', 'no-store');
    return res.sendStatus(204);
  }
  
  next();
});
```

**Solution CDN (CloudFront):**
```yaml