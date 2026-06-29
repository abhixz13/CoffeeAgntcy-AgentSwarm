# ============================================================
# AgentSwarm Demo - Status Check Script (PowerShell)
# ============================================================
# Usage: .\demo_status.ps1
# ============================================================

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "       AGENTSWARM DEMO STATUS CHECK" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# Check Docker Containers
# ============================================================
Write-Host "DOCKER CONTAINERS:" -ForegroundColor Yellow
Write-Host "-" * 50

$containers = @("agentswarm-jaeger", "agentswarm-grafana", "agentswarm-prometheus", "agentswarm-otel-collector")
foreach ($container in $containers) {
    $status = docker ps --filter "name=$container" --format "{{.Status}}" 2>&1
    if ($status -match "Up") {
        Write-Host "  [OK] $container - $status" -ForegroundColor Green
    } else {
        Write-Host "  [--] $container - NOT RUNNING" -ForegroundColor Red
    }
}

# ============================================================
# Check Agent Ports
# ============================================================
Write-Host ""
Write-Host "AGENT SERVICES:" -ForegroundColor Yellow
Write-Host "-" * 50

$services = @(
    @{Port=8000; Name="Orchestrator"; URL="http://localhost:8000"},
    @{Port=8001; Name="Knowledge Agent"; URL="http://localhost:8001"},
    @{Port=8002; Name="CRM Agent"; URL="http://localhost:8002"},
    @{Port=8003; Name="Ticket Agent"; URL="http://localhost:8003"},
    @{Port=8004; Name="Escalation Agent"; URL="http://localhost:8004"}
)

foreach ($svc in $services) {
    $listening = netstat -ano 2>$null | Select-String ":$($svc.Port).*LISTENING"
    if ($listening) {
        Write-Host "  [OK] $($svc.Name) - Port $($svc.Port)" -ForegroundColor Green
    } else {
        Write-Host "  [--] $($svc.Name) - Port $($svc.Port) NOT LISTENING" -ForegroundColor Red
    }
}

# ============================================================
# Dashboard URLs
# ============================================================
Write-Host ""
Write-Host "DASHBOARD URLs:" -ForegroundColor Yellow
Write-Host "-" * 50
Write-Host "  Jaeger (Traces):    http://localhost:16686" -ForegroundColor White
Write-Host "  Grafana (Metrics):  http://localhost:3001  (admin/admin)" -ForegroundColor White
Write-Host "  Prometheus:         http://localhost:9090" -ForegroundColor White
Write-Host "  Orchestrator API:   http://localhost:8000" -ForegroundColor White

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
