### 8.3 Monitoring et Alertes

**Implémentation Telemetry Basique:**
```javascript
// background.js - tracking errors
const errorLog = [];

function logError(context, error) {
  const entry = {
    timestamp: Date.now(),
    context,
    error: {
      name: error.name,
      message: error.message,
      stack: error.stack
    }
  };
  
  errorLog.push(entry);
  
  // Limiter taille log
  if (errorLog.length > 100) {
    errorLog.shift();
  }
  
  // Persister
  chrome.storage.local.set({ errorLog });
  
  // Envoyer au backend (optionnel)
  if (shouldReportError(error)) {
    reportErrorToBackend(entry).catch(console.error);
  }
}

function shouldReportError(error) {
  // Ne pas rapporter erreurs réseau normales
  if (error.name === 'TypeError' && error.message.includes('fetch')) {
    return false;
  }
  return true;
}

async function reportErrorToBackend(errorEntry) {
  try {
    const backendUrl = await getBackendUrl();
    await fetch(`${backendUrl}/api/telemetry/errors`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(errorEntry)
    });
  } catch (e) {
    // Ignorer erreurs reporting
    console.warn('Failed to report error:', e);
  }
}

// Wrapper global errors
self.addEventListener('error', (event) => {
  logError('global', event.error);
});

self.addEventListener('unhandledrejection', (event) => {
  logError('promise', event.reason);
});
```

**Dashboard Errors (options.html):**
```html
<div class="config-section">
  <h2>📊 Diagnostics</h2>
  <button id="showErrors">Afficher Journal Erreurs</button>
  <button id="clearErrors">Effacer Erreurs</button>
  <button id="exportErrors">Exporter pour Support</button>
  <pre id="errorDisplay" style="max-height: 300px; overflow-y: auto;"></pre>
</div>
```
```javascript
// options.js
document.getElementById('showErrors').addEventListener('click', async () => {
  const { errorLog } = await chrome.storage.local.get('errorLog');
  const display = document.getElementById('errorDisplay');
  
  if (!errorLog || errorLog.length === 0) {
    display.textContent = 'Aucune erreur enregistrée';
    return;
  }
  
  display.textContent = JSON.stringify(errorLog, null, 2);
});

document.getElementById('exportErrors').addEventListener('click', async () => {
  const { errorLog } = await chrome.storage.local.get('errorLog');
  const blob = new Blob([JSON.stringify(errorLog, null, 2)], {
    type: 'application/json'
  });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = `extension-errors-${Date.now()}.json`;
  a.click();
});
```

---
