@echo off
echo ========================================
echo   NETTOYAGE DES FICHIERS INUTILISES
echo ========================================
echo.
echo Ce script va:
echo   1. Creer un dossier archives/
echo   2. Deplacer les fichiers de backup
echo   3. Supprimer les fichiers de debug JS
echo   4. Nettoyer les fichiers de log
echo.
echo Gain d'espace estime: ~600 KB
echo.
pause

REM Creer le dossier archives s'il n'existe pas
if not exist "archives" mkdir archives
echo [OK] Dossier archives/ cree

REM 1. DEPLACER LES FICHIERS DE BACKUP PYTHON
echo.
echo [1/4] Deplacement des fichiers de backup Python...
if exist "app_backup.py" move /Y "app_backup.py" "archives\" >nul 2>&1
if exist "app_backup_before_subfolder_support.py" move /Y "app_backup_before_subfolder_support.py" "archives\" >nul 2>&1
if exist "app_before_mapping.py" move /Y "app_before_mapping.py" "archives\" >nul 2>&1
if exist "app_test.py" move /Y "app_test.py" "archives\" >nul 2>&1
echo [OK] Fichiers Python archives

REM 2. DEPLACER LES FICHIERS DE BACKUP HTML
echo.
echo [2/4] Deplacement des fichiers de backup HTML...
if exist "index.html.backup" move /Y "index.html.backup" "archives\" >nul 2>&1
if exist "index_final_stable_20250919_084153.html" move /Y "index_final_stable_20250919_084153.html" "archives\" >nul 2>&1
echo [OK] Fichiers HTML archives

REM 3. DEPLACER LES FICHIERS DE BACKUP BAT
echo.
echo [3/4] Deplacement des fichiers de backup BAT...
if exist "START.bat.backup" move /Y "START.bat.backup" "archives\" >nul 2>&1
if exist "START_original.bat" move /Y "START_original.bat" "archives\" >nul 2>&1
echo [OK] Fichiers BAT archives

REM 4. DEPLACER LE DUPLICATE search-server.js
echo.
echo [4/4] Deplacement du duplicate search-server.js...
if exist "search-server.js" move /Y "search-server.js" "archives\" >nul 2>&1
echo [OK] search-server.js archive (utiliser search-server-fixed.js)

REM 5. SUPPRIMER LES FICHIERS DE DEBUG JAVASCRIPT
echo.
echo [5/7] Suppression des fichiers de debug JavaScript...
del /Q debug_*.js >nul 2>&1
del /Q diagnostic_*.js >nul 2>&1
del /Q check_*.js >nul 2>&1
del /Q fix_modal_buttons.js >nul 2>&1
del /Q modal_buttons_fix_summary.js >nul 2>&1
echo [OK] Fichiers de debug JS supprimes

REM 6. NETTOYER LES FICHIERS DE LOG
echo.
echo [6/7] Nettoyage des fichiers de log...
del /Q *.log >nul 2>&1
del /Q server.pid >nul 2>&1
echo [OK] Fichiers de log nettoyes

REM 7. SUPPRIMER LE FICHIER node VIDE
echo.
echo [7/7] Suppression du fichier node vide...
if exist "node" del /Q "node" >nul 2>&1
echo [OK] Fichier node supprime

echo.
echo ========================================
echo   NETTOYAGE TERMINE !
echo ========================================
echo.
echo Fichiers archives dans: archives\
echo Fichiers de debug supprimes
echo Fichiers de log nettoyes
echo.
echo Verifiez que l'application fonctionne toujours:
echo   1. Lancez START.bat
echo   2. Testez l'application
echo   3. Si tout fonctionne, vous pouvez supprimer archives\
echo.
pause
