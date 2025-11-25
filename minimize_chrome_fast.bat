@echo off
REM Script ULTRA-RAPIDE pour minimiser Chrome et ouvrir l'explorateur
REM Usage: minimize_chrome_fast.bat "C:\path\to\folder"

set "FOLDER_PATH=%~1"

if "%FOLDER_PATH%"=="" (
    exit /b 1
)

REM Ouvrir l'explorateur IMMÉDIATEMENT
start "" "explorer.exe" "%FOLDER_PATH%"

REM Minimiser Chrome en arrière-plan (sans attendre, sans affichage)
powershell -WindowStyle Hidden -Command "Get-Process chrome -ErrorAction SilentlyContinue | ForEach-Object { $hwnd = $_.MainWindowHandle; if ($hwnd -ne [IntPtr]::Zero) { Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class Win32 { [DllImport(\"user32.dll\")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow); }'; [Win32]::ShowWindow($hwnd, 6) } }" > nul 2>&1

exit /b 0
