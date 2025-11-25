# Script de démarrage du Deuxième Cerveau - Structure Organisée
# Version 2.0 - Structure src/ avec compatibilité

param(
    [int]$FlaskPort = 5008,
    [int]$SearchPort = 3008,
    [switch]$NoBrowser
)

Write-Host "=== DEMARRAGE DU DEUXIEME CERVEAU - STRUCTURE ORGANISEE v2.0 ==="
Write-Host "=" * 60

# Fonction de vérification des prérequis
function Test-Prerequisites {
    Write-Host "`n[INFO] Verification des prerequis..."

    # Python
    try {
        $pythonVersion = python --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Python detecte" -ForegroundColor Green
        } else {
            throw "Python non trouve"
        }
    } catch {
        Write-Host "[ERROR] Python non trouve" -ForegroundColor Red
        return $false
    }

    # Flask
    try {
        python -c "import flask" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Flask disponible" -ForegroundColor Green
        } else {
            throw "Flask non disponible"
        }
    } catch {
        Write-Host "[ERROR] Flask non disponible" -ForegroundColor Red
        return $false
    }

    # Node.js
    try {
        $nodeVersion = node --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Node.js detecte" -ForegroundColor Green
        } else {
            throw "Node.js non trouve"
        }
    } catch {
        Write-Host "[ERROR] Node.js non trouve" -ForegroundColor Red
        return $false
    }

    return $true
}

# Fonction de préparation des fichiers
function Prepare-Files {
    Write-Host "`n[INFO] Preparation des fichiers..."

    # Synchroniser les fichiers depuis src/ vers la racine
    if (Test-Path "src\backend\app.py") {
        Copy-Item "src\backend\*" "." -Force
        Write-Host "[OK] Fichiers backend synchronises" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Dossier src/backend non trouve" -ForegroundColor Red
        return $false
    }

    if (Test-Path "src\frontend\index.html") {
        Copy-Item "src\frontend\*" "." -Force
        Write-Host "[OK] Fichiers frontend synchronises" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Dossier src/frontend non trouve" -ForegroundColor Red
        return $false
    }

    return $true
}

# Fonction de démarrage du serveur de recherche
function Start-SearchServer {
    Write-Host "`n[SEARCH] Demarrage du serveur de recherche (port $SearchPort)..."

    # Vérifier que search-server.js existe
    if (-not (Test-Path "search-server.js")) {
        Write-Host "[ERROR] search-server.js non trouve" -ForegroundColor Red
        return $false
    }

    # Démarrer le serveur en arrière-plan
    try {
        $searchJob = Start-Job -ScriptBlock {
            param($Port)
            Set-Location $using:PWD
            node search-server.js
        } -ArgumentList $SearchPort

        Start-Sleep -Seconds 2

        # Vérifier que le serveur répond
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:$SearchPort/status" -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Host "[OK] Serveur de recherche actif sur port $SearchPort" -ForegroundColor Green
                return $true
            }
        } catch {
            Write-Host "[WARNING] Serveur de recherche demarre mais reponse lente" -ForegroundColor Yellow
            return $true
        }
    } catch {
        Write-Host "[ERROR] Echec du demarrage du serveur de recherche: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }

    return $false
}

# Fonction de démarrage du serveur Flask
function Start-FlaskServer {
    Write-Host "`n[FLASK] Demarrage du serveur Flask (port $FlaskPort)..."

    # Vérifier que app.py existe
    if (-not (Test-Path "app.py")) {
        Write-Host "[ERROR] app.py non trouve" -ForegroundColor Red
        return $false
    }

    # Démarrer Flask en arrière-plan
    try {
        $flaskJob = Start-Job -ScriptBlock {
            param($Port)
            Set-Location $using:PWD
            $env:FLASK_ENV = "development"
            python app.py
        } -ArgumentList $FlaskPort

        Start-Sleep -Seconds 3

        # Vérifier que Flask répond
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:$FlaskPort" -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Host "[OK] Serveur Flask actif sur port $FlaskPort" -ForegroundColor Green
                Write-Host "URL: http://localhost:$FlaskPort" -ForegroundColor Cyan
                return $true
            }
        } catch {
            Write-Host "[WARNING] Serveur Flask demarre mais reponse lente" -ForegroundColor Yellow
            Write-Host "URL: http://localhost:$FlaskPort" -ForegroundColor Cyan
            return $true
        }
    } catch {
        Write-Host "[ERROR] Echec du demarrage du serveur Flask: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }

    return $false
}

# Fonction d'ouverture du navigateur
function Open-Browser {
    if (-not $NoBrowser) {
        Write-Host "`n[BROWSER] Ouverture du navigateur..."
        try {
            Start-Process "http://localhost:$FlaskPort"
            Write-Host "[OK] Navigateur ouvert" -ForegroundColor Green
        } catch {
            Write-Host "[WARNING] Impossible d'ouvrir le navigateur automatiquement" -ForegroundColor Yellow
        }
    }
}

# Fonction d'affichage du statut
function Show-Status {
    Write-Host "`n[STATUS] Statut des services:" -ForegroundColor Cyan
    Write-Host "  Flask Server: http://localhost:$FlaskPort" -ForegroundColor White
    Write-Host "  Search Server: http://localhost:$SearchPort" -ForegroundColor White
    Write-Host "  Frontend: src/frontend/" -ForegroundColor White
    Write-Host "  Backend: src/backend/" -ForegroundColor White
    Write-Host "  Tests: src/tests/" -ForegroundColor White

    Write-Host "`n[COMMANDS] Commandes disponibles:" -ForegroundColor Yellow
    Write-Host "  Arreter: Ctrl+C" -ForegroundColor White
    Write-Host "  Tests: .\src\tests\run_integration_tests.bat" -ForegroundColor White
    Write-Host "  Logs: Get-Job | Receive-Job" -ForegroundColor White
}

# Script principal
try {
    # Verifier les prerequis
    if (-not (Test-Prerequisites)) {
        Write-Host "`n[ERROR] Prerequis non satisfaits. Installation requise." -ForegroundColor Red
        exit 1
    }

    # Preparer les fichiers
    if (-not (Prepare-Files)) {
        Write-Host "`n[ERROR] Preparation des fichiers echouee." -ForegroundColor Red
        exit 1
    }

    # Démarrer le serveur de recherche
    $searchStarted = Start-SearchServer

    # Démarrer le serveur Flask
    $flaskStarted = Start-FlaskServer

    if ($flaskStarted) {
        # Ouvrir le navigateur
        Open-Browser

        # Afficher le statut
        Show-Status

        Write-Host "`n[SUCCESS] Deuxieme Cerveau demarre avec succes !" -ForegroundColor Green
        Write-Host "Appuyez sur Ctrl+C pour arreter tous les services." -ForegroundColor Yellow

        # Garder le script actif pour maintenir les jobs
        try {
            while ($true) {
                Start-Sleep -Seconds 1
            }
        } finally {
            Write-Host "`n[STOP] Arret des services..." -ForegroundColor Yellow
            Get-Job | Stop-Job
            Get-Job | Remove-Job
            Write-Host "[OK] Services arretes" -ForegroundColor Green
        }
    } else {
        Write-Host "`n[ERROR] Echec du demarrage des services." -ForegroundColor Red
        Get-Job | Stop-Job
        Get-Job | Remove-Job
        exit 1
    }

} catch {
    Write-Host "`n[CRITICAL] Erreur critique: $($_.Exception.Message)" -ForegroundColor Red
    Get-Job | Stop-Job
    Get-Job | Remove-Job
    exit 1
}
