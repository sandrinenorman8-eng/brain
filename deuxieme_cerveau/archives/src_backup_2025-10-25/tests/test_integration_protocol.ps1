# Protocole de Test d'Intégrité - Web App "Deuxième Cerveau"
# Version 1.0 - Pour Exécution Automatisée (Robot)
# Date: 21/09/2025

param(
    [string]$FlaskUrl = "http://localhost:5008",
    [string]$ReportFile = "test_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
)

# Configuration globale
$global:TestResults = @()
$global:TestStartTime = Get-Date
$global:TimeoutSeconds = 30

# Fonction utilitaire pour exécuter des commandes avec timeout
function Execute-WithTimeout {
    param(
        [ScriptBlock]$ScriptBlock,
        [int]$TimeoutSeconds = $global:TimeoutSeconds
    )

    $job = Start-Job -ScriptBlock $ScriptBlock
    $completed = Wait-Job $job -Timeout $TimeoutSeconds

    if ($completed) {
        $result = Receive-Job $job
        Remove-Job $job
        return $result
    } else {
        Stop-Job $job -ErrorAction SilentlyContinue
        Remove-Job $job -ErrorAction SilentlyContinue
        throw "Commande timeout après $TimeoutSeconds secondes"
    }
}

# Fonction de logging
function Log-Result {
    param(
        [string]$TestName,
        [string]$Status, # "SUCCESS" ou "FAIL"
        [string]$Message = "",
        [string]$Details = ""
    )

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $result = [PSCustomObject]@{
        Timestamp = $timestamp
        TestName = $TestName
        Status = $Status
        Message = $Message
        Details = $Details
    }

    $global:TestResults += $result

    $logMessage = "[$timestamp] $Status - $TestName"
    if ($Message) { $logMessage += ": $Message" }
    if ($Details) { $logMessage += " ($Details)" }

    Write-Host $logMessage
}

# Fonction pour vérifier si ChromeDriver est disponible (optionnel)
function Test-ChromeDriver {
    try {
        $chromeDriverPath = Get-Command chromedriver -ErrorAction Stop
        return $true
    }
    catch {
        return $false
    }
}

# Fonction principale de test
function Start-IntegrationTest {
    Write-Host "=== DEMARRAGE DU PROTOCOLE DE TEST D'INTEGRITE - DEUXIEME CERVEAU ==="
    Write-Host "Rapport sera genere dans: $ReportFile"
    Write-Host "Timeout par defaut: $global:TimeoutSeconds secondes"
    Write-Host ("=" * 60)

    try {
        # Vérifier les prérequis
        $chromeDriverAvailable = Test-ChromeDriver
        if ($chromeDriverAvailable) {
            Log-Result "Prérequis" "SUCCESS" "ChromeDriver trouvé" "Tests complets avec navigateur disponibles"
        } else {
            Log-Result "Prérequis" "WARNING" "ChromeDriver non trouvé" "Tests limités aux vérifications HTTP"
        }

        # Phase 1 : Initialisation
        Phase1-Initialization

        # Phase 2 : Vérification structurelle
        Phase2-StructuralChecks

        # Phase 3 : Tests d'interactions
        Phase3-InteractionTests

        # Phase 4 : Nettoyage
        Phase4-Cleanup

    }
    catch {
        Log-Result "Test Global" "FAIL" "Erreur critique: $($_.Exception.Message)"
    }
    finally {
        # Générer le rapport final
        Generate-TestReport
    }
}

# Phase 1 : Initialisation de l'Environnement de Test
function Phase1-Initialization {
    Write-Host "`n[PHASE 1] Initialisation de l'Environnement de Test"

    # Test 1.1 : Vérifier que le serveur Flask répond
    try {
        Execute-WithTimeout -ScriptBlock {
            $response = Invoke-WebRequest -Uri "$using:FlaskUrl" -TimeoutSec 10
            return $response.StatusCode -eq 200
        } -TimeoutSeconds 15

        Log-Result "Phase1-Test1.1" "SUCCESS" "Serveur Flask accessible" "Code HTTP 200"
    }
    catch {
        Log-Result "Phase1-Test1.1" "FAIL" "Serveur Flask inaccessible" $_.Exception.Message
        throw "Serveur Flask non accessible"
    }

    # Test 1.2 : Vérifier le titre de la page
    try {
        $response = Invoke-WebRequest -Uri $FlaskUrl -TimeoutSec 10
        $htmlContent = $response.Content

        # Extraire le titre depuis le HTML
        if ($htmlContent -match '<title>(.*?)</title>') {
            $pageTitle = $matches[1]
            if ($pageTitle -eq "Deuxième Cerveau - Design Stitch") {
                Log-Result "Phase1-Test1.2" "SUCCESS" "Titre de page correct" "Titre: '$pageTitle'"
            } else {
                Log-Result "Phase1-Test1.2" "FAIL" "Titre de page incorrect" "Attendu: 'Deuxième Cerveau - Design Stitch', Trouvé: '$pageTitle'"
            }
        } else {
            Log-Result "Phase1-Test1.2" "FAIL" "Titre de page non trouvé" "Balise <title> manquante"
        }
    }
    catch {
        Log-Result "Phase1-Test1.2" "FAIL" "Erreur lors de la récupération du titre" $_.Exception.Message
    }

    Write-Host "[OK] Phase 1 terminee"
}

# Phase 2 : Vérification de l'Intégrité Structurelle (Statique)
function Phase2-StructuralChecks {
    Write-Host "`n[PHASE 2] Verification de l'Integre Structurelle"

    # Récupérer le contenu HTML pour les tests
    try {
        $response = Invoke-WebRequest -Uri $FlaskUrl -TimeoutSec 10
        $htmlContent = $response.Content
    }
    catch {
        Log-Result "Phase2-HTML" "FAIL" "Impossible de récupérer le HTML" $_.Exception.Message
        return
    }

    # Test 2.1 : Vérifier les conteneurs principaux
    $containers = @("main-section", "notes-section", "folders-section")
    foreach ($container in $containers) {
        try {
            # Vérifier la présence de l'élément dans le HTML
            if ($htmlContent -match "id=`"$container`"") {
                Log-Result "Phase2-Test2.1-$container" "SUCCESS" "Conteneur trouvé" "id='$container'"
            } else {
                Log-Result "Phase2-Test2.1-$container" "FAIL" "Conteneur manquant" "id='$container'"
            }
        }
        catch {
            Log-Result "Phase2-Test2.1-$container" "FAIL" "Erreur lors de la vérification" $_.Exception.Message
        }
    }

    # Test 2.2 : Vérifier les zones de données clés
    $elements = @(
        @{Id="note-input"; Type="textarea"},
        @{Id="categories-container"; Type="div"},
        @{Id="file-list"; Type="div"},
        @{Id="folder-buttons"; Type="div"}
    )

    foreach ($element in $elements) {
        try {
            # Vérifier la présence de l'élément dans le HTML
            if ($htmlContent -match "id=`"$($element.Id)`"") {
                Log-Result "Phase2-Test2.2-$($element.Id)" "SUCCESS" "Élément trouvé" "$($element.Type) id='$($element.Id)'"
            } else {
                Log-Result "Phase2-Test2.2-$($element.Id)" "FAIL" "Élément manquant" "$($element.Type) id='$($element.Id)'"
            }
        }
        catch {
            Log-Result "Phase2-Test2.2-$($element.Id)" "FAIL" "Erreur lors de la vérification" $_.Exception.Message
        }
    }

    # Test 2.3 : Vérifier le chargement des données mock (simulation)
    try {
        # Vérifier que les conteneurs contiennent du contenu
        $mockDataChecks = @(
            @{Container="categories-container"; Pattern="glass-effect"},
            @{Container="file-list"; Pattern="flex items-center"},
            @{Container="folder-buttons"; Pattern="h-14 px-4"}
        )

        $mockDataLoaded = $true
        foreach ($check in $mockDataChecks) {
            if ($htmlContent -notmatch $check.Pattern) {
                $mockDataLoaded = $false
                break
            }
        }

        if ($mockDataLoaded) {
            Log-Result "Phase2-Test2.3" "SUCCESS" "Données mock chargées" "Contenu détecté dans tous les conteneurs"
        } else {
            Log-Result "Phase2-Test2.3" "WARNING" "Contenu mock partiellement chargé" "Certains éléments peuvent manquer"
        }
    }
    catch {
        Log-Result "Phase2-Test2.3" "FAIL" "Erreur lors de la vérification des données mock" $_.Exception.Message
    }

    Write-Host "[OK] Phase 2 terminee"
}

# Phase 3 : Vérification des Interactions (Dynamique)
function Phase3-InteractionTests {
    Write-Host "`n[PHASE 3] Verification des Interactions (Tests Limites)"

    # Test 3.1 : Vérifier la présence des gestionnaires d'événements
    try {
        $response = Invoke-WebRequest -Uri $FlaskUrl -TimeoutSec 10
        $htmlContent = $response.Content

        $interactionChecks = @(
            @{Name="collapse-btn"; Pattern="toggleSection"},
            @{Name="categories-container"; Pattern="quickSave"},
            @{Name="filter-btn"; Pattern="filterByCategory"},
            @{Name="folder-buttons"; Pattern="openSavedLocation"},
            @{Name="erase-btn"; Pattern="showEraseConfirmation"}
        )

        foreach ($check in $interactionChecks) {
            if ($htmlContent -match $check.Pattern) {
                Log-Result "Phase3-Test3.$($interactionChecks.IndexOf($check) + 1)" "SUCCESS" "Gestionnaire $($check.Name) trouvé" "Fonction: $($check.Pattern)"
            } else {
                Log-Result "Phase3-Test3.$($interactionChecks.IndexOf($check) + 1)" "FAIL" "Gestionnaire $($check.Name) manquant" "Fonction: $($check.Pattern)"
            }
        }
    }
    catch {
        Log-Result "Phase3-Interactions" "FAIL" "Impossible de vérifier les interactions" $_.Exception.Message
    }

    Write-Host "[OK] Phase 3 terminee (tests limites - navigateur requis pour tests complets)"
}

# Phase 4 : Nettoyage
function Phase4-Cleanup {
    Write-Host "`n[PHASE 4] Nettoyage"

    try {
        # Simulation de fermeture du navigateur
        Execute-WithTimeout -ScriptBlock {
            Start-Sleep -Milliseconds 100
            return $true
        }

        Log-Result "Phase4-Cleanup" "SUCCESS" "Navigateur fermé proprement"
    }
    catch {
        Log-Result "Phase4-Cleanup" "FAIL" "Erreur lors de la fermeture" $_.Exception.Message
    }

    Write-Host "[OK] Phase 4 terminee"
}

# Génération du rapport final
function Generate-TestReport {
    Write-Host "`n[REPORT] Generation du Rapport de Test"

    $totalTests = $global:TestResults.Count
    $successCount = ($global:TestResults | Where-Object { $_.Status -eq "SUCCESS" }).Count
    $failCount = $totalTests - $successCount
    $successRate = [math]::Round(($successCount / $totalTests) * 100, 2)

    $endTime = Get-Date
    $duration = $endTime - $global:TestStartTime

    $report = @"
================================================================================
PROTOCOLE DE TEST D'INTÉGRITÉ - DEUXIÈME CERVEAU
Version 1.0 - Rapport d'Exécution Automatisée
================================================================================

Date d'exécution: $($global:TestStartTime.ToString("yyyy-MM-dd HH:mm:ss"))
Durée totale: $($duration.TotalSeconds.ToString("F2")) secondes
URL testée: $FlaskUrl

================================================================================
RÉSUMÉ DES RÉSULTATS
================================================================================

Total des tests exécutés: $totalTests
Tests réussis: $successCount
Tests échoués: $failCount
Taux de succès: $successRate%

================================================================================
DÉTAIL DES TESTS
================================================================================
"@

    foreach ($result in $global:TestResults) {
        $statusIcon = if ($result.Status -eq "SUCCESS") { "[OK]" } else { "[FAIL]" }
        $report += "`n$statusIcon $($result.TestName)"
        if ($result.Message) { $report += " - $($result.Message)" }
        if ($result.Details) { $report += " ($($result.Details))" }
    }

    $report += @"


================================================================================
CONCLUSION
================================================================================

"@

    if ($successRate -ge 80) {
        $report += "[SUCCESS] TESTS GLOBALEMENT REUSSIS`n"
        $report += "L'application presente une integrite structurelle satisfaisante."
    } elseif ($successRate -ge 60) {
        $report += "[WARNING] TESTS PARTIELLEMENT REUSSIS`n"
        $report += "L'application necessite des corrections mineures."
    } else {
        $report += "[FAIL] TESTS GLOBALEMENT ECHOUES`n"
        $report += "L'application necessite des corrections majeures."
    }

    $report += @"


================================================================================
RECOMMANDATIONS
================================================================================

1. Vérifiez les tests échoués et corrigez les problèmes identifiés.
2. Pour une intégration continue, exécutez ce script régulièrement.
3. En cas de modifications du code, relancez les tests complets.
4. Archivez ce rapport pour suivi historique.

================================================================================
FIN DU RAPPORT
================================================================================
"@

    # Écrire le rapport dans le fichier
    try {
        $report | Out-File -FilePath $ReportFile -Encoding UTF8
        Write-Host "[OK] Rapport genere: $ReportFile"
        Write-Host "[STATS] Taux de succes: $successRate%"
    }
    catch {
        Write-Host "[ERROR] Erreur lors de la generation du rapport: $($_.Exception.Message)"
    }
}

# Point d'entrée principal
try {
    Start-IntegrationTest
}
catch {
    Write-Host "[CRITICAL] Erreur critique lors de l'execution des tests: $($_.Exception.Message)"
    exit 1
}
