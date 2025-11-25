@echo off
REM Script RAPIDE pour minimiser Chrome et ouvrir l'explorateur
REM Usage: minimize_chrome.bat "C:\path\to\folder"

set "FOLDER_PATH=%~1"

if "%FOLDER_PATH%"=="" (
    echo Erreur: Aucun chemin fourni
    exit /b 1
)

REM VERSION RAPIDE - Minimiser Chrome et ouvrir l'explorateur en parallèle
start "" "explorer.exe" "%FOLDER_PATH%"

REM Minimiser Chrome en arrière-plan (sans attendre)
powershell -Command "Get-Process chrome -ErrorAction SilentlyContinue | ForEach-Object { $hwnd = $_.MainWindowHandle; if ($hwnd -ne [IntPtr]::Zero) { Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class Win32 { [DllImport(\"user32.dll\")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow); }'; [Win32]::ShowWindow($hwnd, 6) } }" > nul 2>&1

exit /b 0
