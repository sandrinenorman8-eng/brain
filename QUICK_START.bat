@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   EXTENSION CHROME - QUICK START
echo ========================================
echo.
echo Que veux-tu faire ?
echo.
echo 1. Voir le Quick Start (5 sections prioritaires)
echo 2. Lister toutes les sections
echo 3. Voir ma progression
echo 4. Lire une section spécifique
echo 5. Ouvrir tasks.md dans Notepad
echo 6. Ouvrir START_HERE.md
echo 7. Quitter
echo.
set /p choice="Ton choix (1-7) : "

if "%choice%"=="1" (
    python quick_nav.py quick
    pause
    goto menu
)
if "%choice%"=="2" (
    python quick_nav.py list
    pause
    goto menu
)
if "%choice%"=="3" (
    python update_progress.py show
    pause
    goto menu
)
if "%choice%"=="4" (
    set /p section="Numéro de section (1-67) : "
    python quick_nav.py %section%
    pause
    goto menu
)
if "%choice%"=="5" (
    start notepad tasks.md
    goto menu
)
if "%choice%"=="6" (
    start notepad START_HERE.md
    goto menu
)
if "%choice%"=="7" (
    exit
)

:menu
cls
goto :eof
