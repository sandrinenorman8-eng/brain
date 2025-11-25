# Volet 3 : Fallback Auto-Start OS - Windows Task Scheduler
# Script PowerShell pour configurer le démarrage automatique de Memobrik

param(
    [Parameter(Mandatory=$false)]
    [string]$Action = "install",
    
    [Parameter(Mandatory=$false)]
    [string]$ServerPath = "G:\memobrik\deuxieme_cerveau",
    
    [Parameter(Mandatory=$false)]
    [string]$TaskName = "MemobrikAutoStart"
)

# Configuration
$ErrorActionPreference = "Stop"
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogFile = Join-Path $ScriptPath "task_scheduler.log"

# Fonction de logging
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Write-Host $LogEntry
    Add-Content -Path $LogFile -Value $LogEntry
}

# Fonction pour vérifier les privilèges administrateur
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Fonction pour créer le script de démarrage
function New-StartupScript {
    $StartupScriptPath = Join-Path $ScriptPath "memobrik_startup.ps1"
    
    $StartupScriptContent = @"
# Script de démarrage automatique Memobrik
# Généré automatiquement le $(Get-Date)

param(
    [Parameter(Mandatory=`$false)]
    [int]`$MaxRetries = 3,
    
    [Parameter(Mandatory=`$false)]
    [int]`$RetryDelay = 10
)

`$ErrorActionPreference = "Continue"
`$ServerPath = "$ServerPath"
`$LogFile = Join-Path (Split-Path -Parent `$MyInvocation.MyCommand.Path) "startup.log"

function Write-StartupLog {
    param([string]`$Message)
    `$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    `$LogEntry = "[`$Timestamp] `$Message"
    Write-Host `$LogEntry
    Add-Content -Path `$LogFile -Value `$LogEntry -ErrorAction SilentlyContinue
}

function Test-ServerRunning {
    try {
        `$Response = Invoke-WebRequest -Uri "http://localhost:5008/health" -TimeoutSec 5 -UseBasicParsing
        return `$Response.StatusCode -eq 200
    } catch {
        return `$false
    }
}

function Start-MemobrikServer {
    Write-StartupLog "🚀 Tentative de démarrage du serveur Memobrik..."
    
    # Vérifier si le serveur est déjà en cours
    if (Test-ServerRunning) {
        Write-StartupLog "✅ Serveur déjà en cours d'exécution"
        return `$true
    }
    
    # Vérifier que le chemin existe
    if (-not (Test-Path `$ServerPath)) {
        Write-StartupLog "❌ Chemin du serveur non trouvé: `$ServerPath"
        return `$false
    }
    
    # Démarrer le serveur
    try {
        `$StartScript = Join-Path `$ServerPath "START.bat"
        if (-not (Test-Path `$StartScript)) {
            Write-StartupLog "❌ Script de démarrage non trouvé: `$StartScript"
            return `$false
        }
        
        Write-StartupLog "🔄 Démarrage du serveur via `$StartScript"
        
        # Démarrer en arrière-plan
        Start-Process -FilePath `$StartScript -WorkingDirectory `$ServerPath -WindowStyle Hidden
        
        # Attendre que le serveur soit prêt
        `$MaxWait = 30
        `$WaitCount = 0
        
        while (`$WaitCount -lt `$MaxWait) {
            Start-Sleep -Seconds 2
            `$WaitCount += 2
            
            if (Test-ServerRunning) {
                Write-StartupLog "✅ Serveur démarré avec succès (après `$WaitCount secondes)"
                return `$true
            }
            
            Write-StartupLog "⏳ Attente du serveur... (`$WaitCount/`$MaxWait secondes)"
        }
        
        Write-StartupLog "⚠️ Timeout: serveur non prêt après `$MaxWait secondes"
        return `$false
        
    } catch {
        Write-StartupLog "❌ Erreur lors du démarrage: `$(`$_.Exception.Message)"
        return `$false
    }
}

# Script principal
Write-StartupLog "🌅 Démarrage automatique Memobrik initié"
Write-StartupLog "📁 Chemin du serveur: `$ServerPath"

`$Success = `$false
for (`$Retry = 1; `$Retry -le `$MaxRetries; `$Retry++) {
    Write-StartupLog "🔄 Tentative `$Retry/`$MaxRetries"
    
    `$Success = Start-MemobrikServer
    
    if (`$Success) {
        Write-StartupLog "🎉 Démarrage automatique réussi !"
        break
    } else {
        if (`$Retry -lt `$MaxRetries) {
            Write-StartupLog "⏳ Attente de `$RetryDelay secondes avant nouvelle tentative..."
            Start-Sleep -Seconds `$RetryDelay
        }
    }
}

if (-not `$Success) {
    Write-StartupLog "❌ Échec du démarrage automatique après `$MaxRetries tentatives"
    
    # Optionnel: Envoyer une notification
    try {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.MessageBox]::Show(
            "Impossible de démarrer automatiquement le serveur Memobrik.`nVeuillez le démarrer manuellement.",
            "Memobrik Auto-Start",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Warning
        )
    } catch {
        # Ignorer les erreurs de notification
    }
}

Write-StartupLog "🏁 Script de démarrage automatique terminé"
"@

    Set-Content -Path $StartupScriptPath -Value $StartupScriptContent -Encoding UTF8
    Write-Log "Script de démarrage créé: $StartupScriptPath"
    return $StartupScriptPath
}

# Fonction pour installer la tâche planifiée
function Install-ScheduledTask {
    param([string]$ScriptPath)
    
    Write-Log "📅 Installation de la tâche planifiée '$TaskName'..."
    
    try {
        # Supprimer la tâche existante si elle existe
        $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
        if ($ExistingTask) {
            Write-Log "🗑️ Suppression de la tâche existante..."
            Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        }
        
        # Créer l'action
        $Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$ScriptPath`""
        
        # Créer le déclencheur (au démarrage de session)
        $Trigger = New-ScheduledTaskTrigger -AtLogOn
        
        # Créer les paramètres
        $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
        
        # Créer le principal (utilisateur actuel)
        $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
        
        # Enregistrer la tâche
        Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Démarrage automatique du serveur Memobrik au démarrage de session"
        
        Write-Log "✅ Tâche planifiée '$TaskName' installée avec succès"
        
        # Vérifier l'installation
        $InstalledTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
        if ($InstalledTask) {
            Write-Log "✅ Vérification: Tâche trouvée dans le planificateur"
            Write-Log "📋 État: $($InstalledTask.State)"
            return $true
        } else {
            Write-Log "❌ Erreur: Tâche non trouvée après installation"
            return $false
        }
        
    } catch {
        Write-Log "❌ Erreur lors de l'installation: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Fonction pour désinstaller la tâche planifiée
function Uninstall-ScheduledTask {
    Write-Log "🗑️ Désinstallation de la tâche planifiée '$TaskName'..."
    
    try {
        $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
        if ($ExistingTask) {
            Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
            Write-Log "✅ Tâche '$TaskName' désinstallée avec succès"
            return $true
        } else {
            Write-Log "⚠️ Tâche '$TaskName' non trouvée"
            return $true
        }
    } catch {
        Write-Log "❌ Erreur lors de la désinstallation: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Fonction pour tester la tâche planifiée
function Test-ScheduledTask {
    Write-Log "🧪 Test de la tâche planifiée '$TaskName'..."
    
    try {
        $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
        if (-not $Task) {
            Write-Log "❌ Tâche '$TaskName' non trouvée"
            return $false
        }
        
        Write-Log "📋 Informations de la tâche:"
        Write-Log "   - État: $($Task.State)"
        Write-Log "   - Dernière exécution: $($Task.LastRunTime)"
        Write-Log "   - Prochaine exécution: $($Task.NextRunTime)"
        
        # Exécuter la tâche manuellement pour test
        Write-Log "🚀 Exécution manuelle de la tâche pour test..."
        Start-ScheduledTask -TaskName $TaskName
        
        Write-Log "✅ Tâche exécutée. Vérifiez les logs pour les résultats."
        return $true
        
    } catch {
        Write-Log "❌ Erreur lors du test: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Script principal
Write-Log "🎯 Memobrik Windows Task Scheduler - Action: $Action"

# Vérifier les privilèges administrateur pour certaines actions
if ($Action -eq "install" -or $Action -eq "uninstall") {
    if (-not (Test-Administrator)) {
        Write-Log "❌ Privilèges administrateur requis pour cette action" "ERROR"
        Write-Host "Relancez PowerShell en tant qu'administrateur" -ForegroundColor Red
        exit 1
    }
}

# Vérifier que le chemin du serveur existe
if ($Action -eq "install" -and -not (Test-Path $ServerPath)) {
    Write-Log "❌ Chemin du serveur non trouvé: $ServerPath" "ERROR"
    exit 1
}

# Exécuter l'action demandée
switch ($Action.ToLower()) {
    "install" {
        Write-Log "📦 Installation du démarrage automatique..."
        $StartupScript = New-StartupScript
        $Success = Install-ScheduledTask -ScriptPath $StartupScript
        
        if ($Success) {
            Write-Log "🎉 Installation terminée avec succès !"
            Write-Log "💡 Le serveur Memobrik démarrera automatiquement à la prochaine connexion"
            Write-Log "📄 Logs de démarrage: $(Join-Path $ScriptPath 'startup.log')"
        } else {
            Write-Log "❌ Échec de l'installation" "ERROR"
            exit 1
        }
    }
    
    "uninstall" {
        $Success = Uninstall-ScheduledTask
        if ($Success) {
            Write-Log "🎉 Désinstallation terminée avec succès !"
        } else {
            Write-Log "❌ Échec de la désinstallation" "ERROR"
            exit 1
        }
    }
    
    "test" {
        $Success = Test-ScheduledTask
        if (-not $Success) {
            exit 1
        }
    }
    
    "status" {
        try {
            $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
            if ($Task) {
                Write-Log "✅ Tâche '$TaskName' trouvée"
                Write-Log "📋 État: $($Task.State)"
                Write-Log "📅 Dernière exécution: $($Task.LastRunTime)"
                Write-Log "⏰ Prochaine exécution: $($Task.NextRunTime)"
            } else {
                Write-Log "❌ Tâche '$TaskName' non installée"
            }
        } catch {
            Write-Log "❌ Erreur lors de la vérification: $($_.Exception.Message)" "ERROR"
        }
    }
    
    default {
        Write-Log "❌ Action inconnue: $Action" "ERROR"
        Write-Host @"
Usage: .\windows_task_scheduler.ps1 -Action <action>

Actions disponibles:
  install   - Installer le démarrage automatique
  uninstall - Désinstaller le démarrage automatique  
  test      - Tester la tâche planifiée
  status    - Vérifier l'état de la tâche

Exemples:
  .\windows_task_scheduler.ps1 -Action install
  .\windows_task_scheduler.ps1 -Action status
  .\windows_task_scheduler.ps1 -Action uninstall
"@ -ForegroundColor Yellow
        exit 1
    }
}

Write-Log "🏁 Script terminé"