# ============================================================
# AgentSwarm Demo - Full Startup Script (PowerShell)
# ============================================================
# Usage: Right-click -> Run with PowerShell
#    OR: .\demo_start.ps1 in PowerShell terminal
# ============================================================

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "       AGENTSWARM MULTI-AGENT DEMO STARTUP" -ForegroundColor Cyan
Write-Host "       Powered by AGNTCY + Cisco CIRCUIT AI" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath
Write-Host "[INFO] Working directory: $scriptPath" -ForegroundColor Gray

# ============================================================
# STEP 1: Check Docker
# ============================================================
Write-Host ""
Write-Host "[1/5] Checking Docker..." -ForegroundColor Yellow

$dockerRunning = $false
try {
    $dockerInfo = docker info 2>&1
    if ($dockerInfo -match "Server Version") {
        $dockerRunning = $true
        Write-Host "  [OK] Docker is running" -ForegroundColor Green
    }
} catch {}

if (-not $dockerRunning) {
    Write-Host "  [!!] Docker is NOT running!" -ForegroundColor Red
    Write-Host "  Please start Docker Desktop and run this script again." -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# ============================================================
# STEP 2: Start Observability Stack (Docker)
# ============================================================
Write-Host ""
Write-Host "[2/5] Starting Observability Stack (Jaeger, Grafana, Prometheus)..." -ForegroundColor Yellow

docker-compose -f docker-compose.observability.yaml up -d 2>&1 | Out-Null

# Wait and verify
Start-Sleep -Seconds 5
$containers = docker ps --format "{{.Names}}" 2>&1
$expectedContainers = @("agentswarm-jaeger", "agentswarm-grafana", "agentswarm-prometheus", "agentswarm-otel-collector")
$allRunning = $true

foreach ($container in $expectedContainers) {
    if ($containers -match $container) {
        Write-Host "  [OK] $container" -ForegroundColor Green
    } else {
        Write-Host "  [!!] $container NOT running" -ForegroundColor Red
        $allRunning = $false
    }
}

if (-not $allRunning) {
    Write-Host "  [WARN] Some containers failed to start. Check Docker logs." -ForegroundColor Yellow
}

# ============================================================
# STEP 3: Start AI Agents
# ============================================================
Write-Host ""
Write-Host "[3/5] Starting AI Agents..." -ForegroundColor Yellow

# Kill any existing Python processes on our ports (optional cleanup)
# Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "  Starting Knowledge Agent (Port 8001)..." -ForegroundColor Gray
Start-Process cmd -ArgumentList '/k', 'title Knowledge Agent && python agents/knowledge/server.py' -WindowStyle Normal

Write-Host "  Starting CRM Agent (Port 8002)..." -ForegroundColor Gray
Start-Process cmd -ArgumentList '/k', 'title CRM Agent && python agents/crm/server.py' -WindowStyle Normal

Write-Host "  Starting Ticket Agent (Port 8003)..." -ForegroundColor Gray
Start-Process cmd -ArgumentList '/k', 'title Ticket Agent && python agents/ticket/server.py' -WindowStyle Normal

Write-Host "  Starting Escalation Agent (Port 8004)..." -ForegroundColor Gray
Start-Process cmd -ArgumentList '/k', 'title Escalation Agent && python agents/escalation/server.py' -WindowStyle Normal

Write-Host "  Waiting for agents to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 4

# ============================================================
# STEP 4: Start Orchestrator & Bot Gateway
# ============================================================
Write-Host ""
Write-Host "[4/5] Starting Orchestrator & Webex Bot..." -ForegroundColor Yellow

Write-Host "  Starting Orchestrator (Port 8000)..." -ForegroundColor Gray
Start-Process cmd -ArgumentList '/k', 'title Orchestrator && python agents/orchestrator/main.py' -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host "  Starting Webex Bot Gateway..." -ForegroundColor Gray
Start-Process cmd -ArgumentList '/k', 'title Webex Bot Gateway && python webex/bot_gateway.py' -WindowStyle Normal

Start-Sleep -Seconds 2

# ============================================================
# STEP 5: Verify & Open Dashboards
# ============================================================
Write-Host ""
Write-Host "[5/5] Verifying services..." -ForegroundColor Yellow

# Check ports
$ports = @(
    @{Port=8000; Name="Orchestrator"},
    @{Port=8001; Name="Knowledge Agent"},
    @{Port=8002; Name="CRM Agent"},
    @{Port=8003; Name="Ticket Agent"},
    @{Port=8004; Name="Escalation Agent"}
)

Start-Sleep -Seconds 2

foreach ($p in $ports) {
    $listening = netstat -ano | Select-String ":$($p.Port).*LISTENING"
    if ($listening) {
        Write-Host "  [OK] $($p.Name) on port $($p.Port)" -ForegroundColor Green
    } else {
        Write-Host "  [!!] $($p.Name) on port $($p.Port) - NOT READY" -ForegroundColor Red
    }
}

# ============================================================
# DONE - Open Dashboards
# ============================================================
Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "       DEMO READY!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  DASHBOARDS:" -ForegroundColor Cyan
Write-Host "    Jaeger (Traces):   http://localhost:16686" -ForegroundColor White
Write-Host "    Grafana (Metrics): http://localhost:3001  (admin/admin)" -ForegroundColor White
Write-Host ""
Write-Host "  TEST QUERIES (send to Webex bot):" -ForegroundColor Cyan
Write-Host "    Simple:  Hi, I'm customer #67890 and I forgot my password" -ForegroundColor White
Write-Host "    Full:    URGENT: Enterprise #11111, network down, 50 employees!" -ForegroundColor White
Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""

# Ask to open dashboards
$openDashboards = Read-Host "Open dashboards in browser? (Y/N)"
if ($openDashboards -eq "Y" -or $openDashboards -eq "y") {
    Start-Process "http://localhost:16686"
    Start-Process "http://localhost:3001"
    Write-Host ""
    Write-Host "  Dashboards opened in browser!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Press Enter to exit (agents will keep running)..."
Read-Host
