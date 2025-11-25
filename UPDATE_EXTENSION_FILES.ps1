# Script pour adapter l'extension au backend GAE

$BACKEND_URL = "https://top-operand-473602-h0.uc.r.appspot.com"
$EXT_PATH = "G:\memobrik\extchrome"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ADAPTATION EXTENSION POUR GAE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Créer config.js
Write-Host "[1/4] Creation config.js..." -ForegroundColor Yellow
$configContent = @"
// Configuration du backend
const BACKEND_URL = '$BACKEND_URL';
"@
Set-Content -Path "$EXT_PATH\config.js" -Value $configContent
Write-Host "  OK" -ForegroundColor Green

# 2. Modifier background.js
Write-Host "[2/4] Modification background.js..." -ForegroundColor Yellow
$bgContent = @"
// Configuration backend
const BACKEND_URL = '$BACKEND_URL';

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
"@
Set-Content -Path "$EXT_PATH\background.js" -Value $bgContent
Write-Host "  OK" -ForegroundColor Green

# 3. Modifier sidepanel.html
Write-Host "[3/4] Modification sidepanel.html..." -ForegroundColor Yellow
$htmlContent = Get-Content "$EXT_PATH\sidepanel.html" -Raw
$htmlContent = $htmlContent -replace 'src="http://localhost:5008/index.html"', "src=`"$BACKEND_URL`""
$htmlContent = $htmlContent -replace '<script src="loader.js"></script>', "<script src=`"config.js`"></script>`n    <script src=`"loader.js`"></script>"
Set-Content -Path "$EXT_PATH\sidepanel.html" -Value $htmlContent
Write-Host "  OK" -ForegroundColor Green

# 4. Modifier loader.js pour utiliser le backend GAE
Write-Host "[4/4] Modification loader.js..." -ForegroundColor Yellow
$loaderContent = Get-Content "$EXT_PATH\loader.js" -Raw
$loaderContent = $loaderContent -replace 'http://localhost:5008', $BACKEND_URL
$loaderContent = $loaderContent -replace 'http://localhost:5009', $BACKEND_URL
Set-Content -Path "$EXT_PATH\loader.js" -Value $loaderContent
Write-Host "  OK" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ADAPTATION TERMINEE !" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend URL: $BACKEND_URL" -ForegroundColor Green
Write-Host "Extension: $EXT_PATH" -ForegroundColor Green
Write-Host ""
Write-Host "PROCHAINES ETAPES:" -ForegroundColor Yellow
Write-Host "1. Chrome > chrome://extensions/" -ForegroundColor White
Write-Host "2. Recharger 'Deuxieme Cerveau'" -ForegroundColor White
Write-Host "3. Cliquer sur l'icone pour tester" -ForegroundColor White
Write-Host ""
