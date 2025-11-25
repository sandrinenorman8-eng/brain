// Vérifier que le serveur est accessible
const iframe = document.getElementById('app-frame');
const errorMessage = document.getElementById('error-message');

console.log('[DEBUG] Loader initialized');
console.log('[DEBUG] Checking server availability at ' + BACKEND_URL);
console.log('[DEBUG] Current implementation only shows error after 3 second timeout');

// Timeout pour détecter si le serveur ne répond pas
const timeout = setTimeout(() => {
    console.log('[DEBUG] Server timeout reached - server not responding');
    console.log('[DEBUG] Current behavior: hide iframe and show error message');
    console.log('[DEBUG] No mechanism to start servers from extension');
    iframe.style.display = 'none';
    errorMessage.classList.add('show');
}, 3000);

// Si l'iframe charge correctement, annuler le timeout
iframe.addEventListener('load', () => {
    console.log('[DEBUG] iFrame loaded successfully');
    clearTimeout(timeout);
    errorMessage.classList.remove('show');
    iframe.style.display = 'block';
});

// Gérer les erreurs de chargement
iframe.addEventListener('error', () => {
    console.log('[DEBUG] iFrame failed to load');
    console.log('[DEBUG] Current behavior: hide iframe and show error message');
    clearTimeout(timeout);
    iframe.style.display = 'none';
    errorMessage.classList.add('show');
});

