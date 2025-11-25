### 7.4 Problème: Erreurs CSP Silencieuses

**Symptôme:**
Requêtes fetch échouent sans erreur explicite
Console Chrome: violations CSP ignorées
Network tab: requêtes marquées "(blocked:csp)"

**Cause:**
Typos ou incohérences dans `content_security_policy`

**Erreurs Fréquentes:**
```json
// ❌ INCORRECT - Espace après point-virgule
{
  "content_security_policy": {
    "extension_pages": "connect-src 'self' https://backend.com; "
    // Espace final invalide ^
  }
}

// ❌ INCORRECT - Directive manquante
{
  "content_security_policy": {
    "extension_pages": "script-src 'self';" 
    // Manque: object-src, connect-src
  }
}

// ❌ INCORRECT - URL sans protocole
{
  "content_security_policy": {
    "extension_pages": "connect-src 'self' backend.com;"
    // Doit être: https://backend.com
  }
}

// ❌ INCORRECT - Incohérence extension_pages vs content_scripts
{
  "content_security_policy": {
    "extension_pages": "connect-src 'self' https://api1.com;",
    "content_scripts": "connect-src 'self' https://api2.com;"
    // Différentes APIs, risque de bugs
  }
}
```

**✅ Configuration Correcte:**
```json
{
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'; connect-src 'self' https://your-backend.vercel.app https://*.ngrok-free.app https://accounts.google.com;",
    "content_scripts": "script-src 'self'; object-src 'self';"
  }
}
```

**Validation CSP:**
```javascript
// Test script dans background.js
console.log('Testing CSP compliance...');

// Test 1: Fetch autorisé
fetch('https://your-backend.vercel.app/api/health')
  .then(r => console.log('✅ Backend fetch OK'))
  .catch(e => console.error('❌ Backend fetch blocked:', e));

// Test 2: Fetch non-autorisé (doit échouer)
fetch('https://unauthorized-domain.com/api')
  .then(r => console.warn('⚠️ Unauthorized fetch succeeded - CSP too permissive'))
  .catch(e => console.log('✅ Unauthorized fetch correctly blocked'));

// Test 3: OAuth domain
fetch('https://accounts.google.com')
  .then(r => console.log('✅ OAuth domain accessible'))
  .catch(e => console.error('❌ OAuth domain blocked:', e));
```

**Debugging CSP:**

Ouvrir DevTools → Console
Filtrer: "csp"
Chercher: "Refused to connect to"
Identifier domaine bloqué
Ajouter à connect-src
Recharger extension

