@echo off
set "chromePath=C:\Program Files\Google\Chrome\Application\chrome.exe"
set "debugPort=9222"
set "userDataDir=C:\temp\chrome-debug"

if not exist "%userDataDir%" mkdir "%userDataDir%"

start "" "%chromePath%" --remote-debugging-port=%debugPort% --user-data-dir="%userDataDir%" --load-extension=./extension

timeout /t 2 /nobreak >nul
curl http://localhost:9222/json/version