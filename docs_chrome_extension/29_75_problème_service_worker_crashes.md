### 7.5 Problème: Service Worker Crashes

**Symptôme:**
Extension cesse de répondre après quelques minutes
Background script ne traite plus messages
chrome.runtime.sendMessage timeout

**Cause:**
Service workers Chrome ont cycle de vie strict (inactif après 30s sans événement)

**Solution: Keep-Alive Pattern**
```javascript
// background.js - maintenir service worker actif
let keepAliveInterval;

function startKeepAlive() {
  // Ping toutes les 20 secondes
  keepAliveInterval = setInterval(() => {
    chrome.runtime.getPlatformInfo(() => {
      // Vide - juste pour maintenir worker actif
    });
  }, 20000);
}

function stopKeepAlive() {
  if (keepAliveInterval) {
    clearInterval(keepAliveInterval);
  }
}

// Démarrer au chargement
startKeepAlive();

// Gérer extinction navigateur
chrome.runtime.onSuspend.addListener(() => {
  stopKeepAlive();
  console.log('Service worker suspending...');
});

// Re-démarrer au réveil
chrome.runtime.onStartup.addListener(() => {
  startKeepAlive();
  console.log('Service worker restarted');
});
```

**Alternative: Alarms API**
```javascript
// Utiliser chrome.alarms (persiste après suspension)
chrome.alarms.create('keepAlive', { 
  periodInMinutes: 0.5 // 30 secondes
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'keepAlive') {
    // Vérifier santé backend
    checkBackendHealth().catch(console.error);
  }
});
```
