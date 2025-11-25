/**
 * Memobrik Auto-Starter - Background Service Worker
 * Volet 1 Phase C : Modification Extension
 */

const SERVER_PORT = 5008;
const SERVER_URL = `http://localhost:${SERVER_PORT}`;
const NATIVE_HOST = 'com.memobrik.server_starter';
const MAX_RETRY_ATTEMPTS = 3;

// État global
let isServerStarting = false;
let retryCount = 0;

/**
 * Vérifie si le serveur est accessible
 */
async function checkServerHealth() {
  try {
    const response = await fetch(`${SERVER_URL}/health`, {
      method: 'GET',
      cache: 'no-store',
      signal: AbortSignal.timeout(3000)
    });
    return response.ok;
  } catch (error) {
    console.log('Serveur non accessible:', error.message);
    return false;
  }
}

/**
 * Attend que le serveur soit prêt avec timeout
 */
async function waitUntilServerReady(timeoutMs = 20000) {
  const startTime = performance.now();
  
  while (performance.now() - startTime < timeoutMs) {
    try {
      const isReady = await checkServerHealth();
      if (isReady) {
        console.log('✅ Serveur prêt !');
        return true;
      }
    } catch (error) {
      console.log('Vérification serveur échouée:', error);
    }
    
    // Attendre 500ms avant la prochaine vérification
    await new Promise(resolve => setTimeout(resolve, 500));
  }
  
  throw new Error(`Timeout: serveur non prêt après ${timeoutMs}ms`);
}

/**
 * Démarre le serveur via Native Messaging
 */
async function startServerViaHost() {
  return new Promise((resolve, reject) => {
    console.log('🚀 Connexion au Native Messaging Host...');
    
    const port = chrome.runtime.connectNative(NATIVE_HOST);
    let responseReceived = false;
    
    // Timeout de sécurité
    const timeout = setTimeout(() => {
      if (!responseReceived) {
        port.disconnect();
        reject(new Error('Timeout Native Messaging'));
      }
    }, 30000);
    
    port.onMessage.addListener((response) => {
      responseReceived = true;
      clearTimeout(timeout);
      
      console.log('📨 Réponse Native Host:', response);
      
      if (response.status === 'started' || response.status === 'already_running') {
        resolve(response);
      } else {
        reject(new Error(response.message || `Erreur: ${response.status}`));
      }
      
      port.disconnect();
    });
    
    port.onDisconnect.addListener(() => {
      responseReceived = true;
      clearTimeout(timeout);
      
      if (chrome.runtime.lastError) {
        console.error('❌ Erreur Native Messaging:', chrome.runtime.lastError);
        reject(new Error(chrome.runtime.lastError.message));
      } else {
        reject(new Error('Connexion fermée par l\'hôte'));
      }
    });
    
    // Envoyer la commande de démarrage
    port.postMessage({ action: 'start_server' });
  });
}

/**
 * Ouvre le side panel
 */
async function openSidePanel() {
  try {
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tabs.length > 0) {
      await chrome.sidePanel.open({ tabId: tabs[0].id });
      console.log('📱 Side panel ouvert');
    }
  } catch (error) {
    console.error('❌ Erreur ouverture side panel:', error);
    // Fallback: ouvrir dans un nouvel onglet
    await chrome.tabs.create({ url: SERVER_URL });
  }
}

/**
 * Affiche une notification
 */
function showNotification(title, message, type = 'basic') {
  chrome.notifications.create({
    type: type,
    iconUrl: 'icons/icon48.png',
    title: title,
    message: message
  });
}

/**
 * Fonction principale pour démarrer le serveur
 */
async function ensureServerRunning() {
  if (isServerStarting) {
    console.log('⏳ Démarrage déjà en cours...');
    return;
  }
  
  isServerStarting = true;
  
  try {
    console.log('🔍 Vérification de l\'état du serveur...');
    
    // Vérifier si le serveur est déjà en cours
    const isAlreadyRunning = await checkServerHealth();
    
    if (isAlreadyRunning) {
      console.log('✅ Serveur déjà en cours d\'exécution');
      await openSidePanel();
      return;
    }
    
    console.log('🚀 Démarrage du serveur...');
    showNotification('Memobrik', 'Démarrage du serveur en cours...', 'basic');
    
    // Démarrer le serveur via Native Messaging
    const response = await startServerViaHost();
    console.log('✅ Serveur démarré:', response);
    
    // Attendre que le serveur soit prêt
    console.log('⏳ Attente de la disponibilité du serveur...');
    await waitUntilServerReady();
    
    // Ouvrir le side panel
    await openSidePanel();
    
    showNotification('Memobrik', 'Serveur démarré avec succès !', 'basic');
    retryCount = 0; // Reset du compteur en cas de succès
    
  } catch (error) {
    console.error('❌ Erreur lors du démarrage:', error);
    
    retryCount++;
    
    if (retryCount <= MAX_RETRY_ATTEMPTS) {
      showNotification(
        'Memobrik - Erreur', 
        `Tentative ${retryCount}/${MAX_RETRY_ATTEMPTS}: ${error.message}`, 
        'basic'
      );
      
      // Retry après 2 secondes
      setTimeout(() => {
        isServerStarting = false;
        ensureServerRunning();
      }, 2000);
    } else {
      showNotification(
        'Memobrik - Échec', 
        `Impossible de démarrer le serveur: ${error.message}`, 
        'basic'
      );
      retryCount = 0;
    }
  } finally {
    isServerStarting = false;
  }
}

/**
 * Gestionnaire de clic sur l'icône de l'extension
 */
chrome.action.onClicked.addListener(async (tab) => {
  console.log('🖱️ Clic sur l\'icône de l\'extension');
  await ensureServerRunning();
});

/**
 * Gestionnaire d'installation de l'extension
 */
chrome.runtime.onInstalled.addListener((details) => {
  console.log('📦 Extension installée:', details);
  
  if (details.reason === 'install') {
    showNotification(
      'Memobrik Auto-Starter', 
      'Extension installée ! Cliquez sur l\'icône pour démarrer le serveur.', 
      'basic'
    );
  }
});

/**
 * Gestionnaire de démarrage de Chrome
 */
chrome.runtime.onStartup.addListener(() => {
  console.log('🌅 Chrome démarré');
  // Optionnel: démarrer automatiquement le serveur au démarrage de Chrome
  // ensureServerRunning();
});

/**
 * Gestionnaire de messages depuis le content script ou popup
 */
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('📨 Message reçu:', message);
  
  if (message.action === 'start_server') {
    ensureServerRunning()
      .then(() => sendResponse({ success: true }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Indique une réponse asynchrone
  }
  
  if (message.action === 'check_server') {
    checkServerHealth()
      .then(isRunning => sendResponse({ isRunning }))
      .catch(error => sendResponse({ isRunning: false, error: error.message }));
    return true;
  }
});

console.log('🎯 Memobrik Auto-Starter Background Script chargé');