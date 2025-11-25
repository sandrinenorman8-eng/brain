# CloudFront Behavior Settings
Cache Policy:
  Query Strings: All
  Headers: 
    - Origin
    - Access-Control-Request-Method
    - Access-Control-Request-Headers
  Cookies: None
  
Cache Key Settings:
  Override for OPTIONS:
    TTL: 0 seconds
    Cache-Control: Respect origin headers
```

**Solution CDN (Cloudflare):**
```javascript
// Cloudflare Worker - bypass cache pour OPTIONS
addEventListener('fetch', event => {
  const request = event.request;
  
  if (request.method === 'OPTIONS') {
    // Bypass cache Cloudflare
    event.respondWith(fetch(request, { cf: { cacheTtl: 0 } }));
  } else {
    event.respondWith(fetch(request));
  }
});
```

**Validation:**
```bash