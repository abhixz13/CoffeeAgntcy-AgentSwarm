# ============================================================
# AgentSwarm Demo - Full Shutdown Script (PowerShell)
# ============================================================
# Usage: Right-click -> Run with PowerShell
#    OR: .\demo_stop.ps1 in PowerShell terminal
# ============================================================

Write-Host ""
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host "       AGENTSWARM DEMO SHUTDOWN" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host ""

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# ============================================================
# STEP 1: Stop Python Agents
# ============================================================
Write-Host "[1/2] Stopping Python agents..." -ForegroundColor Yellow

$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    $pythonProcesses | Stop-Process -Force
    Write-Host "  [OK] Stopped $($pythonProcesses.Count) Python process(es)" -ForegroundColor Green
} else {
    Write-Host "  [OK] No Python processes running" -ForegroundColor Gray
}

# Also close cmd windows with our titles
$cmdWindows = Get-Process cmd -ErrorAction SilentlyContinue
# Note: This will close ALL cmd windows, be careful
# For selective closing, we'd need more complex logic

# ============================================================
# STEP 2: Stop Docker Containers
# ============================================================
Write-Host ""
Write-Host "[2/2] Stopping Docker containers..." -ForegroundColor Yellow

docker-compose -f docker-compose.observability.yaml down 2>&1 | Out-Null

Write-Host "  [OK] Docker containers stopped" -ForegroundColor Green

# ============================================================
# DONE
# ============================================================
Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "       ALL SERVICES STOPPED" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to exit"
