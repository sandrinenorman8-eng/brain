// Configuration backend
const BACKEND_URL = 'https://volitionary-prince-springily.ngrok-free.dev';

// Ouvrir le side panel au clic sur l'icône
chrome.action.onClicked.addListener(async (tab) => {
  console.log('[DEBUG] Extension icon clicked - opening side panel');
  
  try {
    // Vérifier que le backend est accessible
    const response = await fetch(`${BACKEND_URL}/api/health`);
    if (response.ok) {
      console.log('[DEBUG] Backend is online');
    }
  } catch (error) {
    console.warn('[WARNING] Backend check failed:', error);
  }
  
  // Ouvrir le side panel
  chrome.sidePanel.open({ windowId: tab.windowId });
});

// Log quand l'extension est prête
chrome.runtime.onInstalled.addListener(() => {
  console.log('[DEBUG] Extension Deuxième Cerveau installée');
  console.log('[DEBUG] Backend URL:', BACKEND_URL);
});
